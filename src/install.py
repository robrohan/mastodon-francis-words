import os
# os.system("rm -rf TensorFlowTTS")
os.system("git clone https://github.com/TensorSpeech/TensorFlowTTS.git")
os.chdir("TensorFlowTTS")
os.system("pip install .")
os.chdir("..")
