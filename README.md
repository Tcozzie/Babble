# 331-finalProject-Babble
Final Project for 331 Babble app

Partners: Tiegan Cozzie, Burgin Luker, Josh Wilcox, Morgan Hanson

## To start redis server (will need for local development)
1. make sure you have downloaded redis to your system
2. run `redis-server`


# For Tiegan
## EC2 Environment
`source venv/bin/activate`

`tmux attach -t babble`

`tmux new -s babble`

running with Gunicorn
`gunicorn -w 2 app:app`
