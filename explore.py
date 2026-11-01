import pandas as pd
df = pd.read_csv("data/KDDTrain+.txt", header=None)
import pandas as pd

columns = [
    "duration", "protocol_type", "service", "flag", "src_bytes", "dst_bytes",
    "land", "wrong_fragment", "urgent", "hot", "num_failed_logins",
    "logged_in", "num_compromised", "root_shell", "su_attempted", "num_root",
    "num_file_creations", "num_shells", "num_access_files",
    "num_outbound_cmds", "is_host_login", "is_guest_login", "count",
    "srv_count", "serror_rate", "srv_serror_rate", "rerror_rate",
    "srv_rerror_rate", "same_srv_rate", "diff_srv_rate",
    "srv_diff_srv_rate", "dst_host_count", "dst_host_srv_count",
    "dst_host_same_srv_rate", "dst_host_diff_srv_rate",
    "dst_host_same_src_port_rate", "dst_host_srv_diff_host_rate",
    "dst_host_serror_rate", "dst_host_srv_serror_rate",
    "dst_host_rerror_rate", "dst_host_srv_rerror_rate", "label", "difficulty"
]

df = pd.read_csv("data/KDDTrain+.txt", header=None)
df.columns = columns


print(df["label"].value_counts())
print(df.isnull().sum().sum())
attack_map = {
    "normal": "normal",
    "neptune": "DoS", "smurf": "DoS", "back": "DoS",
    "teardrop": "DoS", "pod": "DoS", "land": "DoS",
    "satan": "Probe", "ipsweep": "Probe", "portsweep": "Probe", "nmap": "Probe",
    "guess_passwd": "R2L", "warezclient": "R2L", "warezmaster": "R2L",
    "imap": "R2L", "ftp_write": "R2L", "multihop": "R2L",
    "phf": "R2L", "spy": "R2L",
    "buffer_overflow": "U2R", "rootkit": "U2R",
    "loadmodule": "U2R", "perl": "U2R",
}

df["attack_category"] = df["label"].map(attack_map)

print(df["attack_category"].value_counts())
print(df["attack_category"].isnull().sum())