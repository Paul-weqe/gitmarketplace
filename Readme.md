# GitmarketPlace

Git Marketplace is a Git Repository project, aimed at behaving like Github in a way. 

This guide will take us through the setup process and how to keep maintaining the project. 

## Initializing a Git server. 

First things first, we cannot run Git without having a Git server. A git server will be 
storing the <a href="https://mijingo.com/blog/what-is-a-bare-git-repository">bare repositories</a>. 

Use The following <a href="https://git-scm.com/book/en/v2/Git-on-the-Server-Setting-Up-the-Server">guide</a> to setup your git server 

Once we have our git server set up, we are ready to get running as far as git is concerned.

## Running the MarketPlace itself

To get marketplace running on our dev environment, we first have to install docker and docker compose 
in our system:
1. <a href="https://docs.docker.com/engine/install/ubuntu/">Installing Docker</a>
2. <a href="https://docs.docker.com/engine/install/linux-postinstall/">Post Docker Installation</a>
2. <a href="https://docs.docker.com/compose/install/">Installing Docker Compose</a>

We should now have docker ready to run for our project.

## Getting the environment variables set up
Most of the services environment variables are gotten from the `.env` file. 

So we should create a `.env` file in the root of our project. The following will be it's contents:
```dotenv
POSTGRES_DB=your_db_name
TEST_POSTGRES_DB=your_test_db_name
POSTGRES_USER=your_db_user
POSTGRES_PASSWORD=your_db_password
``` 

<i> Of course, make sure to replace your_db_name, your_test_db_name, your_db_user 
and your_db_password with their respective values depending on what you want</i>

## Get the services up and running

Now, we get the services by running:

```shell
docker-compose up -d web 
```

If everything goes well, you will be able to access GitMarketplace via http://localhost:8000.

You should now be able to create an account and create a repository. One final thing, 
once you have the repository created on gitmarketplace, you can clone it using:
```shell
git clone git@localhost:/home/git/{username}/{repository-name}
```

Still looking for a better way we can clone this repository. 

Once cloned, we can edit the files, add commits, add a branch etc. Once done, we can push 
to the server by running:
```shell
git push origin master
```

At this point, our localhost is the origin, so the contents will be updated on the git 
server(which is our localhost).

When we visit our 127.0.0.1:8000 and login, we can now see all our repositories. Click 
any of the repositories, and you will be able to view the directories, files and 
commits(not yet branches). 

A lot of things may still be a bit shady, but they will be improved upon. 