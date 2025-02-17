#!/usr/bin/env python

#Convert nepi darknet model folder to nepi yolov3 model folder

import os
import shutil
import glob

import converter

MODEL_FOLDER = 'mnt/nepi_storage/ai_models'
DARKNET_MODEL_FOLDER = 'mnt/nepi_storage/ai_models/darknet_ros'
IMG_WIDTH = 


ROMOVE_CFG_LINES = ['jitter','nms_threshold','threshold']

def read_yaml2dict(file_path):
    dict_from_file = dict()
    if os.path.exists(file_path):
        try:
            os.system('chown -R nepi:nepi ' +  file_path)
            with open(file_path) as f:
                dict_from_file = yaml.load(f, Loader=yaml.FullLoader)
        except:
            nepi_msg.publishMsgWarn(self,"Failed to get dict from file: " + file_path + " " + str(e))
    else:
        nepi_msg.publishMsgWarn(self,"Failed to find dict file: " + file_path)
    return dict_from_file

def write_dict2yaml(dict_2_save,file_path,defaultFlowStyle=False,sortKeys=False):
    success = False
    path = os.path.dirname(file_path)
    if os.path.exists(path):
        try:
            with open(file_path, "w") as f:
                yaml.dump(dict_2_save, stream=f, default_flow_style=defaultFlowStyle, sort_keys=sortKeys)
                os.system('chown -R nepi:nepi ' +  file_path)
            success = True
        except:
            nepi_msg.publishMsgWarn(self,"Failed to write dict: " + str(dict_2_save) + " to file: " + file_path + " " + str(e))
    else:
        nepi_msg.publishMsgWarn(self,"Failed to find file path: " + path)
    return success

def create_cfg_mod_file(cfg_file, mod_cfg_file):
    success = True
    img_width = 0
    img_height = 0
    file_lines = []
    try:
        with open(cfg_file, "r") as f:
            for line in f:
                if if any(keyword in line for keyword in ROMOVE_CFG_LINES):
                    pass
                else:
                    if line.find('width') != -1:
                        w_str = line.split('=')[1]
                        img_width = int(w_str)
                    if line.find('height') != -1:
                        h_str = line.split('=')[1]
                        img_height = int(h_str)
                    file_lines.append(line)
        with open(mod_cfg_file, "w") as f:
            for line in file_lines:
                f.write(line)
        os.system('chown -R nepi:nepi ' + mod_cfg_file)
    except Exception as e:
        print('Failed to cretae cfg mod file: ' + mod_cfg_file)
        success = False
    return success


if __name__ == '__main__':
    models_dict = dict()
    if os.path.exists(DARKNET_MODEL_FOLDER) == False:
        print("Darknet model folder not found at: " + str(DARKNET_MODEL_FOLDER))
    else:
        # Creat yolov3 folder
        yolov3_folder = os.path.join(MODEL_FOLDER, 'yolov3')
        if not os.path.isdir(yolov3_folder):
                rospy.logwarn("Tmp folder " + yolov3_folder + " not present... will create")
                os.makedirs(yolov3_folder)
        os.system('chown -R nepi:nepi ' +  yolov3_folder) # Use os.system instead of os.chown to have a recursive option
        os.system('chmod -R 0775 ' + yolov3_folder)
        # Creat tmp folder
        tmp_folder = os.path.join(DARKNET_MODEL_FOLDER, 'tmp')
        if not os.path.isdir(tmp_folder):
                rospy.logwarn("Tmp folder " + tmp_folder + " not present... will create")
                os.makedirs(tmp_folder)
        os.system('chown -R nepi:nepi ' +  tmp_folder) # Use os.system instead of os.chown to have a recursive option
        os.system('chmod -R 0775 ' + tmp_folder)
        # get nepi ai yaml files
        yaml_files = glob.glob(DARKNET_MODEL_FOLDER + '/**/*.yaml',recursive=True)
        cfg_files = glob.glob(DARKNET_MODEL_FOLDER + '/**/*.cfg',recursive=True)
        weight_files = glob.glob(DARKNET_MODEL_FOLDER + '/**/*.weights',recursive=True)
        print("Found darknet yaml config files: " + str(yaml_files))
        for yaml_file in yaml_files:
            model_name = yaml_file.replace('.yaml','')
            models_dict[model_name] = dict()
            yaml_dict = read_yaml2dict(file)
            success = False
            if 'config_file' in yaml_dict.keys() and 'weight_file' in yaml_dict.keys() and 'detection_classe' in yaml_dict.keys():
                model_dict = dict
                model_dict['yaml_file'] = yaml_file
                model_dict['yaml_dict'] = yaml_dict
                for cfg_file in cfg_files:
                    if cfg_file.find(yaml_dict['config_file']) != -1:
                        model_dict['cfg_file'] = cfg_file
                if 'cfg_file' in model_dict.keys():
                    for weight_file in weight_files:
                        if weight_file.find(yaml_dict['weight_file']) != -1:
                            model_dict['weight_file'] = weight_file
                        if 'weight_file' in model_dict.keys(): 
                            model_dict['classes'] = yaml_dict['detection_classes']
                            success = True
                if success:
                  models_dict[model_name] = model_dict
        purge_list = []
        for model_name in models_dict.keys():
            model_dict = models_dict[model_name]
            cfg_file = model_dict['cfg_file']
            file = os.path.basename(cfg_file)
            path = os.path.dirname(cfg_file)
            mod_cfg_file = os.path.join(tmp_folder,file)
            [success,img_width,img_height] = create_cfg_mod_file(cfg_file,mod_cfg_file)
            if success = True and img_width != 0 and img_height != 0 :
                models_dict[model_name]['mod_cfg_file'] = mod_cfg_file
                models_dict[model_name]['yaml_dict']['image_size'] = dict()
                models_dict[model_name]['yaml_dict']['image_size']['image_width'] = img_width
                models_dict[model_name]['yaml_dict']['image_size']['image_height'] = img_height
            else:
                purge_list.append.(model_name)
        for model_name in purge_list:
            del models_dict[model_name]


        # Run conversion
        for model_name in models_dict.keys():
            print('Converting model: ' + str(model_name))
            cfg_file = models_dict[model_name]['mod_cfg_file']
            weight_file = models_dict[model_name]['weight_file']
            yaml_dict = img_width = models_dict[model_name]['yaml_dict']
            img_width = yaml_dict['image_size']['image_width']
            img_height = yaml_dict['image_size']['image_height']
            
            success = converter.convert(output_folder = yolov3_folder, model_name = model_name, cfg='cfg/yolov3-spp.cfg', weights='weights/yolov3-spp.weights',  img_dim=(img_width, img_height))

            if success:
                yaml_save_file = os.path.join(yolov3_folder,model_name,'.yaml')
                if os.path.exists(yaml_save_file):
                    os.remove(yaml_save_file)
                write_dict2yaml(yaml_dict,yaml_save_file):

            
