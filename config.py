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

attack_map = {
    "normal": "normal",
    "neptune": "DoS", "smurf": "DoS", "back": "DoS", "teardrop": "DoS",
    "pod": "DoS", "land": "DoS", "apache2": "DoS", "mailbomb": "DoS",
    "processtable": "DoS", "udpstorm": "DoS", "worm": "DoS",
    "satan": "Probe", "ipsweep": "Probe", "portsweep": "Probe",
    "nmap": "Probe", "mscan": "Probe", "saint": "Probe",
    "guess_passwd": "R2L", "warezclient": "R2L", "warezmaster": "R2L",
    "imap": "R2L", "ftp_write": "R2L", "multihop": "R2L", "phf": "R2L",
    "spy": "R2L", "named": "R2L", "sendmail": "R2L", "snmpgetattack": "R2L",
    "snmpguess": "R2L", "xlock": "R2L", "xsnoop": "R2L",
    "buffer_overflow": "U2R", "rootkit": "U2R", "loadmodule": "U2R",
    "perl": "U2R", "httptunnel": "U2R", "ps": "U2R", "sqlattack": "U2R",
    "xterm": "U2R",
}