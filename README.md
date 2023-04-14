# LoraTrainServer

Lora train with server api

most code from:
 - [bmaltais/kohya_ss](https://github.com/bmaltais/kohya_ss)
 - [kohya-ss/sd-scripts](https://github.com/kohya-ss/sd-scripts)

## Running 
1. clone repo
2. create venv `python -m venv venv` 
3. activate venv `call venv/bin/activate`
4. install requirements
 
`pip install torch==1.12.1+cu116 torchvision==0.13.1+cu116 --extra-index-url https://download.pytorch.org/whl/cu116
pip install --use-pep517 --upgrade -r requirements.txt
pip install -U -I --no-deps https://github.com/C43H66N12O12S2/stable-diffusion-webui/releases/download/f/xformers-0.0.14.dev0-cp310-cp310-win_amd64.whl
`
install for windows
`
copy /y .\bitsandbytes_windows\*.dll .\venv\Lib\site-packages\bitsandbytes\
copy /y .\bitsandbytes_windows\cextension.py .\venv\Lib\site-packages\bitsandbytes\cextension.py
copy /y .\bitsandbytes_windows\main.py .\venv\Lib\site-packages\bitsandbytes\cuda_setup\main.py
`

`accelerate config `

5. run `python -m accelerate.commands.launch api_launcher.py` 
