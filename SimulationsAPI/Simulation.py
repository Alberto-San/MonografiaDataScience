import pandas as pd
import os
import pickle
import paramiko
import scp

class RemoteClient:
    def __init__(self, hostname, username, password, port):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.port=port
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.connect()

    def connect(self):
        self.client.connect(hostname=self.hostname, port=self.port, username=self.username, password=self.password)

    def close(self):
        self.client.close()

    def execute_command(self, command):
        stdin, stdout, stderr = self.client.exec_command(command)
        if stderr is not None:
            print(stderr.read().decode('utf-8'))
        return stdout.read().decode('utf-8')

    def copy_file_to_remote(self, local_path, remote_path):
        scp_client = scp.SCPClient(self.client.get_transport())
        scp_client.put(local_path, remote_path)
        scp_client.close()

class Classifiers():
    def get_instances(self):
        dummy_class = ["classifier_{}".format(index) for index in range(2)]
        return dummy_class

class Scalers():
    def get_instances(self):
        dummy_class = ["scaler_{}".format(index) for index in range(2)]
        return dummy_class

class DimensionalReduction():
    def get_instances(self):
        dummy_class = ["dim_red_{}".format(index) for index in range(2)]
        return dummy_class

class MasterJob():
    def set_up_folders(self):
        folder = "./tmp/MasterJob"
        os.system("rm -rf {}".format(folder))
        os.system("mkdir {}".format(folder))
        
    def compress_data(self, partitions):
        nodes = (partitions.keys())

        # Store data (serialize)
        for node in nodes:
            filename = "./tmp/MasterJob/{}.pickle".format(node)
            data = partitions[node]

            with open(filename, 'wb') as handle:
                pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
    # # Load data (deserialize)
    # with open('filename.pickle', 'rb') as handle:
    #     unserialized_data = pickle.load(handle)

    def send_file_to_remote(self, nodes_info):
        nodes = list(nodes_info.keys())

        for node in nodes:
            host_data = nodes_info[node]
            username = host_data["username"]
            password = host_data["password"]
            filename = "./tmp/MasterJob/{}.pickle".format(node)

            remote_client = RemoteClient(node, username, password)
            remote_client.copy_file_to_remote(filename, '/home/daniel/repository/')

    def send_data_to_nodes(self, partitions, nodes_info):
        self.set_up_folders()
        self.compress_data(partitions)
        self.send_file_to_remote(nodes_info)
        
class Simulation():
    def __init__(
            self
            ,table_path
            ,features
            ,image_path
            ,summary_path
            ,nodes
            ,nodes_user_password
    ):
        self.table_path = table_path
        self.features = features
        self.image_path = image_path
        self.summary_path = summary_path
        self.nodes = nodes
        self.nodes_info = nodes_user_password #{"localhost": {"username": "", password: ""}}

    def get_simulation_data(self, classifiers, scalers, dim_reduction_procesors, table):
        simulation_dic = {}
        simulation_id = 0

        for classifier in classifiers:
            for scaler in scalers:
                for dim_reduction_procesor in dim_reduction_procesors:
                    simulation_dic[simulation_id] = {
                        "classifier": classifier, # attribute classifier, name
                        "scaler": scaler, # # attribute scaler, name
                        "dim_reduction_procesor": dim_reduction_procesor, # attribute dim_reduction_procesor, name,
                        "table": table,
                        "features": self.features
                    }
                    simulation_id += 1

        return simulation_dic
    
    def get_partitions(self, simulation_dic):
        simulation_keys = list(simulation_dic.keys())
        nodes_available = len(self.nodes)
        nodes_data = {}
        index_data = 0

        for simulation_id in simulation_keys:
            simulation_data = simulation_dic[simulation_id]
            node = self.nodes[index_data]

            if node not in list(nodes_data.keys()):
                nodes_data[node] = []

            nodes_data[node].append(simulation_data)
            index_data += 1

            if index_data == nodes_available:
                index_data = 0

        return nodes_data

    def send_data_to_nodes(self, partitions):
        MasterJob().send_data_to_nodes(partitions, self.nodes_info)
    
    def start_jobs_in_remote(self):
        None

    def prepare(self):
        table = pd.read_csv(self.table_path).iloc[:2]
        classifiers = Classifiers().get_instances()
        scalers = Scalers().get_instances()
        dim_reduction_procesors = DimensionalReduction().get_instances()
        simulation_dic = self.get_simulation_data(classifiers, scalers, dim_reduction_procesors, table)
        partitions = self.get_partitions(simulation_dic) # {"0.0.0.0": [ {sim_data1}, {sim_data2}, .... ], "localhost": [ {sim_data3}, {sim_data4}, .... ]}
        self.send_data_to_nodes(partitions) # creates folder on nodes and sends the data

    def run(self):
        self.prepare()
        self.start_jobs_in_remote()


simulation = Simulation(
    table_path="tmp/color_statistics.csv", # /path/to/input_csv
    features="class	image_path	feature_0	feature_1	feature_2	feature_3	feature_4	feature_5	feature_6	feature_7	feature_8	feature_9	feature_10	feature_11	feature_12	feature_13	feature_14	feature_15	feature_16	feature_17	feature_18	feature_19	feature_20	feature_21".split("	"), # / list of features
    image_path="image_path", # field of csv that contains the image_path
    summary_path="output.csv", # /path/to/output_csv
    nodes=["192.168.80.11"], # list of nodes that contains the IP,
    nodes_user_password={
        "192.168.80.11": {
            "username":"daniel",
            "password": "slliskkt09"
        }
    }
)
simulation.run()