Posting stuff on a website/blog is time consuming. Manually posting that stuff to the social sites is another pain.
You can use this robot to automate the process for you.
- It will check for the new content using your [RSS](https://en.wikipedia.org/wiki/RSS) feeds and post the stuff to the social sites.

Currently, it posts the stuff to your page
- facebook page
- twitter account
- telegram channel

notifies the admin, on telegram about the post.

- This application was built on `Python 3.7.5` and `Ubuntu 18.04.3 LTS`.
- I have used `json` files to store secret credentials. You may use other ways like `config` files, `environment variables`, etc. Just edit the code accordingly.

### Getting started:

- `Clone` the respository.

### Creating the Application

Now enter the cloned directory.

#### Facebook

- Create a page on Facebook, in case you don't have one.

- Create an application on [Facebook](https://developers.facebook.com/tools/explorer/)

- Acquire the appropriate permissions so that you have the necessary rights to publish posts on the page.

- Create a file
```bash
touch creds/fb_creds.json
```

- Generate the acess_token and keep it somewhere safe.
    - **Note**: Generate and use `long-lived tokens` as shorter ones expire too soon.

- Note down the page id for your page. You may find it inside Facebook's **Access Token Debugger** or inside the about section of your page when you open it as an administrator. 

- Now paste the values inside the file `fb_creds.json`.

**Format**
```json
{
    "access_token": "MY ACCESS TOKEN",
    "page_id": "MY PAGE ID"
}
```

- As of now, before your application can go live on Facebook, it will require a privacy policy. In case you don't have one, you may generate one using https://www.privacypolicytemplate.net/

#### Twitter

- Create an account on twitter.

- Create an application on [Twitter](https://developer.twitter.com/apps)

- Acquire the appropriate permissions so that you have the necessary right to create status for the user.

- Create a file
```bash
touch creds/twitter_creds.json
```

- Generate the access token.

- Now paste the values inside the file `twitter_creds.json`.

**Format**
```json
{
    "api_key": "MY CONSUMER KEY",
    "api_secret_key": "MY SECRET CONSUMER KEY",
    "access_token_key": "MY ACCESS TOKEN",
    "access_token_secret": "MY SECRET ACCESS TOKEN"
}
```

#### Telegram

- Create a channel on telegram in case you don't have one.

- Use [Bot Father](https://t.me/botfather) to create the telegram bot.

- Generate the access token.

- Make sure the bot has permissions to post messages.

- Send a message to the bot from your admin account(robots can't send you a message unless you message them).

- Send a GET request to `api.telegram.org/bot{MY ACCESS TOKEN}/sendMessage`

    - Note down the `chat_id` from the `response`. This will be used to notify the admin about the postings.

- Now paste the details in the file `telegram_creds.json`

**Format**
```json
{
    "token": "MY TOKEN",
    "username": "USERNAME FOR BOT",
    "channel": "USERNAME FOR CHANNEL",
    "admin_id": "CHAT ID"
}
```

### Installation and setup

- From the cloned directory, create a virtual environment.
```
python3.7 -m venv {PATH TO VIRTUAL ENV}
```

- Activate the environment inside the directory where this application has been cloned.
```bash
source {PATH TO VIRTUAL ENV}/bin/activate
```

- Clone this repository and activate the environment inside this directory.

- Install the requirements.
```python
pip install -r requirements.txt
```

- Create a database. It will be used to store the links that have been posted.
    - I thought it would be quick way to search through the posted links by storing the values inside a database. You may use any other technique.
    In case, it is faster, please bother to contribute.

    - I have used `MySQL`. You may use any other, just edit the file [`db_connect.py`](./db_connect.py) 
    accordingly.

- Set the URL for RSS feed inside the file.

- Create a file `creds_db.json`
```bash
touch creds/creds_db.json
```

- Create a database table and add the details to the `creds_db.json`

**Format**
```json
{
    "database": "NAME OF THE DATABASE",
    "host": "HOST",
    "user": "USER",
    "password": "PASSWORD",
    "table": "NAME OF THE TABLE",
    "column": "NAME OF THE COLUMN THAT WILL STORE LINKS"
}
```

- Create a file `creds_feed.json`
```bash
nano creds/creds_feed.json
```
and add the feed URL.  

**Format**
```json
{
    "SITE_NAME": "THE NAME OF THE WEBSITE",
    "URL": "MY RSS FEED URL"
}
```

- The value of `SITE_NAME` will be used in creating posts.
    
    - The sample template for a post will be:

    
> Checkout this new post from The GitHub Blog: Browse good first issues to start contributing to open source https://github.blog/2020-01-22-browse-good-first-issues-to-start-contributing-to-open-source/


In case you want to customize the message for posts, you may edit the `POST` variable inside [`process_feed.py`](./process_feed.py)

- Initially, to add the entries that are already present on your website, run
```python
python process_feed.py
```
This will add the links to the database.

- Try adding a post to your website(anyhow just add an item to your RSS feed) and test if everything is working well by running
```python
python post_to_social.py
```
If everything went well, you will get a message on telegram from your telegram bot about the response after posting.(I don't know if this is best way to notify the owner about the posting but currently, it is as it is.)  

- Now schedule a [`cron`](https://en.wikipedia.org/wiki/Cron) job for running the script `post_to_social.py` according to your requirements.

TODO
- Add support for LinkedIn.
