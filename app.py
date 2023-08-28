import gradio as gr
from modules.sdxl_styles import style_keys, aspect_ratios
import random
import re
from gradio_client import Client
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("--server_port", help="port number for the server", type=int)
parser.add_argument("--share", help="share or not", type=bool)
parser.add_argument("--server",help="server address", type=str)
args = parser.parse_args()

if args.server_port:
    server_port = args.server_port
else:
    server_port = 8001 
    
if args.share:
    share = args.share
else:
    share = False 

if args.server:
    server = args.server
else:
    server = "https://e2481bfdd6990a82f7.gradio.live" 




    
def welcome(name):
    return 'https://user-images.githubusercontent.com/19834515/260323110-d386f817-4bd7-490c-ad89-c1e228c23447.png'

def generate_random_number():
    return random.randint(0, 999999999999)

def generate_image(prompt="",negative_prompt="", style_selction='cinematic-default', performance_selction='Speed', aspect_ratios_selction='1152×896', image_seed=generate_random_number()):
    client = Client(server,serialize=False,output_dir="./tmp",max_workers=1)
    result = client.predict(
				prompt,	# str in 'parameter_8' Textbox component
				negative_prompt,	# str in 'Negative Prompt' Textbox component
				style_selction,	# str in 'parameter_23' Radio component
				performance_selction,	# str in 'Performance' Radio component
				aspect_ratios_selction,	# str in 'Aspect Ratios (width × height)' Radio component
				1,	# int | float (numeric value between 1 and 32) in 'Image Number' Slider component
				image_seed,	# int | float in 'Seed' Number component
				0,	# int | float (numeric value between 0.0 and 40.0) in 'Sampling Sharpness' Slider component
				"sd_xl_refiner_1.0_0.9vae.safetensors",	# str (Option from: ['sd_xl_refiner_1.0_0.9vae.safetensors', 'sd_xl_base_1.0_0.9vae.safetensors']) in 'SDXL Base Model' Dropdown component
				"None",	# str (Option from: ['None', 'sd_xl_refiner_1.0_0.9vae.safetensors', 'sd_xl_base_1.0_0.9vae.safetensors']) in 'SDXL Refiner' Dropdown component
				"None",	# str (Option from: ['None', 'sd_xl_offset_example-lora_1.0.safetensors']) in 'SDXL LoRA 1' Dropdown component
				-2,	# int | float (numeric value between -2 and 2) in 'Weight' Slider component
				"None",	# str (Option from: ['None', 'sd_xl_offset_example-lora_1.0.safetensors']) in 'SDXL LoRA 2' Dropdown component
				-2,	# int | float (numeric value between -2 and 2) in 'Weight' Slider component
				"None",	# str (Option from: ['None', 'sd_xl_offset_example-lora_1.0.safetensors']) in 'SDXL LoRA 3' Dropdown component
				-2,	# int | float (numeric value between -2 and 2) in 'Weight' Slider component
				"None",	# str (Option from: ['None', 'sd_xl_offset_example-lora_1.0.safetensors']) in 'SDXL LoRA 4' Dropdown component
				-2,	# int | float (numeric value between -2 and 2) in 'Weight' Slider component
				"None",	# str (Option from: ['None', 'sd_xl_offset_example-lora_1.0.safetensors']) in 'SDXL LoRA 5' Dropdown component
				-2,	# int | float (numeric value between -2 and 2) in 'Weight' Slider component
				fn_index=4
    )
    
    path = find_result_image_path(str(result))
    print(result)
    print(str(result))
    if path == None:
        raise gr.Error("Please try again.") 
    else:
        return path
    

##用于测试的字符串 ({'__type__': 'update', 'mode': 'dynamic'}, {'visible': False, '__type__': 'update'}, {'visible': False, '__type__': 'update'}, {'visible': True, 'value': [{'name': '/tmp/gradio/cd0dafe9ca7b8af7febbb86f3761135ce7e6643f/image.png', 'data': None, 'is_file': True}], '__type__': 'update'})
def find_result_image_path(string):
    pattern = r'/tmp.*\.png'
    match = re.search(pattern, string)
    if match:
        return match.group()
    else:
        return None


with gr.Blocks(theme='gradio/soft') as demo:
    gr.Markdown(
    """
    # Black Magic
    The world's best image generator with unbelievable image quality.  
    """)
    

    
    prompt = gr.Textbox(label="Prompt", placeholder="Enter your negative prompt here?", lines=3, max_lines=3)
    
    with gr.Accordion("Advanced Options", open=False):
        negative_prompt = gr.Textbox(label="Negative Prompt",placeholder="Enter your negative prompt here", lines=3, max_lines=3)

        with gr.Row():
            aspect_ratios_selction = gr.Dropdown(label='Aspect Ratios (width × height)', choices=list(aspect_ratios.keys()),    value='1152×896',interactive=True)
            style_selction = gr.Dropdown(label="Styles",show_label=True, container=True, choices=style_keys, value='cinematic-default',interactive=True)
        with gr.Row():
            image_seed = gr.Slider(0,999999999999,label='Seed',value=generate_random_number(), scale=1, interactive=True)
            performance_selction = gr.Radio(label='Performance(Premium Feature)', choices=['Speed', 'Quality'], value='Speed',interactive=False)
            
    btn = gr.Button(value="Generate") 
    
    out = gr.Image()
    
    gr.Markdown(
    """
    <center>Powered by <a href="https://stablediffusionweb.com">Stable Diffusion Web</a> </center>  
    """)
    
    
    btn.click(fn=generate_image,inputs=[prompt,negative_prompt,style_selction,performance_selction,aspect_ratios_selction,image_seed],outputs=out)
    

if __name__ == "__main__":
    demo.queue(concurrency_count=1,status_update_rate=6,api_open=False).launch(show_api=False,share=share, server_port=server_port)