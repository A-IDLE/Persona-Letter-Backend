pkill uvicorn || true

cd ~/Persona_Letter
sudo rm -r ~/Persona_Letter/Persona-Letter-Backend/

git clone https://github.com/A-IDLE/Persona-Letter-Backend.git

cd ~/Persona_Letter/Persona-Letter-Backend/

pip install -r requirements.txt

cp ~/Persona_Letter/config/backend/* ~/Persona_Letter/Persona-Letter-Backend/
cp ~/Persona_Letter/config/backend/.env ~/Persona_Letter/Persona-Letter-Backend/

nohup uvicorn app.main:fastapi_app --host 0.0.0.0 --port 9000 --reload &