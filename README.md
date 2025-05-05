# Customized Comic Strip Generator

Follow these steps to set up the project locally using **Conda**:

##  Clone the Repository

```bash
git clone https://github.com/Chandrahas455/Customized-Comic-Strip-Generator.git
cd Customized_Comic_Strip_Generator
```

##  Create Environment

```bash
conda create --name comicgen python=3.10 -y
conda activate comicgen
```

##  Install Dependencies

```bash
pip install -r requirements.txt
```

##  Add your Gemini API Key in .env

```bash
GEMINI_API_KEY = "PASTE YOUR GEMINI KEY HERE"
```

## CLI Usage

You can  generate the comic strip using the **CLI**  by running the project through a Python script. Here's how to do it:

```bash
python main_cli.py --input path_to_your_image --name "Your Name" --guide "Optional storyline prompt"
```

## Run the Gradio App

Run the Gradio App for easy usage :

```bash
python gradio_app.py
```



