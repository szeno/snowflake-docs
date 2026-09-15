# SnowConvert AI - How to Use SnowConvert AI with Docker

## Dependencies

The following dependencies must be installed on the machine:

- [Docker desktop](https://docs.docker.com/desktop/windows/install/)
- [Visual Code](https://code.visualstudio.com/download)
- [Docker Extension in Visual Code](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-docker)

## Steps

### Create the image config file

Create a file called *“Dockerfile” (no extension)* with the following content. This configuration will be used to build the Docker image.

Copy code

```
FROM ubuntu
COPY snowCli /dockerDestinationFolder
ENV DOTNET_SYSTEM_GLOBALIZATION_INVARIANT=1
RUN apt-get update
RUN apt-get install -y ca-certificates openssl
```

When using the [Ubuntu](https://hub.docker.com/_/ubuntu) image to run the SnowConvert AI CLI for Linux a couple of dependencies must be added to the Dockerfile in order to activate the license, for this purpose [System.Globalization.Invariant](https://docs.microsoft.com/en-us/dotnet/core/run-time-config/globalization) must be turned ON and the OpenSSL must be installed to be able to establish an HTTPS connection for the license validation.

In addition to the dependencies installation, the second line (`COPY` command) is used to copy files from the local machine inside the image. In this case, the *snowCLI* file (located in the same folder as the Dockerfile) will be copied to`/dockerDestinationFolder`inside the image.

### Build the image

Launch Docker Desktop app.

Open Visual Code where the “*Dockerfile”* is located. If you have previously installed the Docker extension for Visual Code, the *“Dockerfile”* will be automatically recognized as a docker configuration file by Visual Code. Right-click on the “Dockerfile” and hit *“Build image…”*

[![](/static/images/migrations/sc-assets/image(212).png)](/static/images/migrations/sc-assets/image(212).png)

This will prompt for a name to give the image, at the top of Visual Code.

[![](/static/images/migrations/sc-assets/image(152).png)](/static/images/migrations/sc-assets/image(152).png)

Use any name you want and hit “*Enter”.* That causes Docker to set up the container, by pulling the Ubuntu image, installing dependencies, copying the specified files. Wait for the terminal to finish. Once you see a message like this one, it means the image was successfully built.

Copy code

```
> Executing task: docker build --pull --rm -f "Dockerfile" -t release:Ubuntu "." <

[+] Building 2.0s (11/11) FINISHED                                                                                           0.0s
.
.
.
```

### Run the image

Go to Docker Desktop in the Images tab, and hit run on the recently created image.

[![](/static/images/migrations/sc-assets/image(162).png)](/static/images/migrations/sc-assets/image(162).png)

Go back to Visual Code, and go to the Docker tab. You should see, under *Containers* the image that was just run. You can expand it and explore the file directory.

[![](/static/images/migrations/sc-assets/image(297).png)](/static/images/migrations/sc-assets/image(297).png)

### Connect to the container

Finally, if you right-click on the running container and hit *“Attach shell”* you will be able to connect to the container in the Terminal and use all your favorite commands.

[![](/static/images/migrations/sc-assets/image(104).png)](/static/images/migrations/sc-assets/image(104).png)

You should see your personal files here that were specified to be copied by the COPY command in the configuration file.
