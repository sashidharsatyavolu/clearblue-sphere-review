# Streamlit Clear Blue-style Interactive Sphere

This version wraps the interactive Three.js sphere inside a Streamlit app so it can be deployed and shared with a public `streamlit.app` URL.

## Local test

```bash
python3 -m pip install -r requirements.txt
streamlit run app.py
```

## Deployment

Push this folder to a GitHub repository, then deploy `app.py` through Streamlit Community Cloud.

The sphere uses Three.js from jsDelivr in the browser.
