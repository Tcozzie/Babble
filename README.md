# 331-finalProject-Babble
Final Project for 331 Babble app

Partners: Tiegan Cozzie, Burgin Luker, Josh Wilcox, Morgan Hanson

## To start redis server (will need for local development)
1. make sure you have downloaded redis to your system
2. run `redis-server`

## Amazon Cognito
To make this app work you will have to create your own amazon cognito user pool.
Sorry that I had to remove mine and make it private. Im unfortunately not a charity LOL

# For Tiegan
## EC2 Environment
`source venv/bin/activate`

`tmux attach -t babble`

`tmux new -s babble`

running with Gunicorn
`gunicorn -w 2 app:app`
