### MangaScan

I ❤️ collecting manga and a lot of other people do too. But my one problem with collecting manga is that it is hard to keep track of what is being released. That is why I created MangaScan, to help you keep track of up and coming releases.

I am currently tracking these publishers:
- **Viz Media**
- **Yen Press**
- **Dark Horse**
- **Seven Seas**
- **Kodansha/Vertical** 

I have to mention that tracking Kodansha is still work in process. It currently works, but without receiving the images of the manga titles.

## Run
You can run MangaScan in few different ways. The first method is using Kubernetes. Open the root folder in your terminal and execute the following command:
```shell script
$ kubectl apply -f k8s
```
After that, the deployments and services will be deployed in your cluster. To run the application, execute the following command:

```shell script
$ minikube service mangascan
```

Note: this was tested with the following versions:<br>
- Minikube (v1.11.0)
- Kubernetes (v1.18.3)
- Docker (19.38)

To run it only with Docker, use the following command:
```shell script
$ docker-compose up
```

to run it locally, use the following commands:
```shell script
# activate python virtual environment
$ python3 -m venv venv
$ source venv/bin/activate

# install needed requirements 
$ pip install -r requirements.txt

# start application 
$ python app.py
```