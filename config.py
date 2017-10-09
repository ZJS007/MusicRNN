import configparser as parser

dict_type = {
	'new_resolution' : int, 
	'bpm' : int,
	'note_chars' : str,
	'separation_char' : str,
	'layer_size' : int,
	'n_layer' : int, 
	'batch_size' : int,
	'seq_size' : int,
	'n_epoch' : int,
	'learning_rate' : float,
	'output_keep_prob' : float,
	'init_from_model' : str,
	'model_save_name' : str,
	'midis_folder_name_list' : lambda x : x.split(';'),
	'n' : int,
	'first_chars' : str,
	'sample_from_model' : str,
	'sample_dir' : str,
	'sample_name': str,
	'mu' : float,
	'sigma' : float
}

parsed_config = parser.ConfigParser(allow_no_value = True)
parsed_config.read('config.ini')

config = {}
for section in parsed_config.sections():
	config[section] = {}
	for key in parsed_config[section]:
		if parsed_config[section][key] is not None:
			config[section][key] = dict_type[key](parsed_config[section][key])
		else:
			config[section][key] = None