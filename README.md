# SADIC Web

**SADIC Web** is a web application running the SADIC app https://pypi.org/project/sadic
https://usiena-air.unisi.it/handle/11365/1263654

---

## 🚀 Getting Started

To start the deployment, run:

```bash
docker-compose up --build
```
## ⚙️ Optional Maintenance Commands

If needed, you can run the following Django management commands:


```bash
docker exec -it sadicweb python3 manage.py flush --noinput
docker exec -it sadicweb python3 manage.py makemigrations
docker exec -it sadicweb python3 manage.py migrate` 
```
----------

## 🖥 Production Deployment

To deploy in detached mode (recommended for production environments):
```bash
docker-compose up --build -d
```
----------


### 🌐 Web Interface

You can also use the admin panel available at:
```
http://localhost:8081
```
----------

## 📦 Project Structure

-   `sadicweb`: Django application container
    
-   `sadic_database`: MariaDB container
    
----------

## 📄 License

This project is licensed under the MIT License.

----------

## 👨‍💻 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.
