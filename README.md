# An Abstract A Day Bot

*"Read one abstract every day and before long you will be very smart"*

### A simple python script to scrape recent abstracts from arXiv.org and send them to you via email

## Dependancies

- python3
- beautifulsoup4

## Usage

Simply run `python3 abstract_email.py` to send one email with random recent articles.

Run as a cron job to recieve daily updates.

## Configuration

Replace `sendtoemail@domain.com` with your email. Replace `sendfromemail@gmail.com` and `myplaintextpassword` with account information of the gmail account you use to send automated emails. Make sure the sending account is [configured to handle SMTP requests](https://stackoverflow.com/questions/10147455/).

Set the subjects (and corresponding urls) you want to recieve abstracts from. By default these are: 
```
Robotics: https://arxiv.org/list/cs.RO/pastweek?show=1000
AI: https://arxiv.org/list/cs.AI/pastweek?show=1000
Systems and Control: https://arxiv.org/list/cs.SY/pastweek?show=1000
Multiagent Systems: https://arxiv.org/list/cs.MA/pastweek?show=1000
Learning: https://arxiv.org/list/cs.LG/pastweek?show=1000
Machine Learning: https://arxiv.org/list/stat.ML/pastweek?show=1000
Computer Vision: https://arxiv.org/list/cs.CV/pastweek?show=1000
Human-Computer Interaction: https://arxiv.org/list/cs.HC/pastweek?show=1000
Formal Languages/Automata Theory: https://arxiv.org/list/cs.FL/pastweek?show=1000
```

