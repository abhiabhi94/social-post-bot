_Posting stuff on a website/blog is time consuming. Manually posting that stuff to the social sites is another pain._

You can use this robot to automate the process for you.
- It will check for the new content using your [RSS](https://en.wikipedia.org/wiki/RSS) feeds and post the stuff to the social sites.

Currently, it posts the stuff to your page
- twitter account.
- telegram channel.
- medium.
- facebook page.

notifies the admin, on telegram about the post.

- This application was built on `Python 3.7.5` and `Ubuntu 18.04.3 LTS`.

### Getting started

- `Clone` the respository.

### Creating the Application

Now enter the cloned directory.

Create a file `.env` to store secrets. You can use the file [.env.template](./.env.template)as a template.

Incase, you don't want to use any of the below mentioned social mediums, just set the environment variable for `USE_{MEDIUM}` to `False` in the `.env` and move ahead.
For e.g, if you aren't interested in facebook, set `USE_FACEBOOK=False` and move to the next section.

#### Twitter

- Create an account on twitter.

- Create an application on [Twitter](https://developer.twitter.com/apps)

- Acquire the appropriate permissions so that you have the necessary right to create status for the user.

- Generate the access token.

- Now paste the values inside the file `.env`.

```env
TWITTER_API_KEY="my_consumer_key"
TWITTER_API_SECRET_KEY="my_secret_consumer_key"
TWITTER_ACCESS_TOKEN_KEY="my_access_token"
TWITTER_ACCESS_TOKEN_SECRET="my_secret_access_token"
```

#### Telegram

- Create a channel on telegram in case you don't have one.

- Use [Bot Father](https://t.me/botfather) to create the telegram bot.

- Generate the access token.

- Make sure the bot has permissions to post messages.

- Send a message to the bot from your admin account(robots can't send you a message unless you message them).

- Send a GET request to `api.telegram.org/bot{MY ACCESS TOKEN}/getUpdates`

    - Note down the `chat_id` from the `response`. This will be used to notify the admin about the postings.

- Now paste the details in the file `.env`.

```env
TELEGRAM_TOKEN="my_token"
TELEGRAM_USERNAME="username_for_bot"
TELEGRAM_CHANNEL="username_for_channel"
TELEGRAM_ADMIN_ID="chat_id"
```

#### Medium

- Create an account on Medium, in case you don't have one.

- Go to your account settings, and go to Integration Token there and generate a token from there.

- Now use this token to get your `user_id` by sending a GET request to the url https://api.medium.com/v1/me and set the above integration token as an authorization header.

An example request would be using `curl` would be:
```sh
curl https://api.medium.com/v1/me  -H "Authorization: Bearer 181d415f34379af07b2c11d144dfbe35d"
# the response
{
  "data": {
      # this is your user_id
    "id": "5303d74c64f66366f00cb9b2a94f3251bf5",
    "username": "majelbstoat",
    "name": "Jamie Talbot",
    "url": "https://medium.com/@majelbstoat",
    "imageUrl": "https://images.medium.com/0*fkfQiTzT7TlUGGyI.png"
  }
}
```
This example values have been taken from the [official medium docs](https://github.com/Medium/medium-api-docs#getting-the-authenticated-users-details). Please refer to them for more information.

- Grab the user_id and add those secrets to the `.env` file.

- In case, your blog has content in the markdown format, set `MARKDOWN_FORMAT=markdown`. The default value is `html`.

- In case you want a line in the end of the sort
```html
<p><i>This was originally posted on <a href='https://www.my-original-website.com' rel='canonical'>MySite</a>.</i></p>'
```
```env
MEDIUM_ACCESS_TOKEN='access_token'
MEDIUM_USER_ID='user_id'
MEDIUM_END_TXT='paste_the_actual_html_or_markdown_here'
```


#### Facebook

- Create a page on Facebook, in case you don't have one.

- Create an application on [Facebook](https://developers.facebook.com/tools/explorer/)

- Acquire the appropriate permissions so that you have the necessary rights to publish posts on the page.

- Generate the acess_token and keep it somewhere safe.
    - **Note**: Generate and use `long-lived tokens` as shorter ones expire too soon.

- Note down the page id for your page. You may find it inside Facebook's **Access Token Debugger** or inside the about section of your page when you open it as an administrator.

- Now paste the values inside the file `.env` file.

```env
FACEBOOK_ACCESS_TOKEN="my_access_token"
FACEBOOK_PAGE_ID="my_page_id"
```

- As of now, before your application can go live on Facebook, it will require a privacy policy. In case you don't have one, you may generate one using https://www.privacypolicytemplate.net/

- You might also need to go through their *App Review* before they allow you to publish posts.


### Installation and setup

- From the cloned directory, create a virtual environment.
```sh
python3 -m venv {PATH TO VIRTUAL ENV}
```

- Activate the environment inside the directory where this application has been cloned.
```sh
. {PATH TO VIRTUAL ENV}/bin/activate
```

- Clone this repository and activate the environment inside this directory.

- Install the requirements.
```sh
pip install -r requirements.txt
```

- Create a database. It will be used to store the links that have been posted.
    - At the time of writing this appplication, it was thought it would be quick way to search through the posted links by storing the values inside a database. You may use any other technique.
    In case, it is faster, please bother to contribute.

    - It uses `MySQL`. You may use any other, just edit the file [`db_connect.py`](./social_post_bot/db_connect.py)
    accordingly.

- Set the URL for RSS feed inside the file.

- Create a database table and add the details to the `.env`

```env
DB_NAME="name_of_the_database"
DB_HOST="host"
DB_USER="user"
DB_PASSWORD="password"
DB_TABLE="name_of_the_table"
DB_COLUMN="name_of_the_column_that_will_store_links"
```

- Add the feed URL.

```env
CUSTOM_TXT="THE TEXT THAT WILL BE PREFIXED BEFORE EVERY POST"
FEED_URL="MY RSS FEED URL"
```

- You may choose to ignore the `CUSTOM_TXT` field, if you don't want to prefix a customary post with every post.

    - In this case, the sample template for a post will be

> Browse good first issues to start contributing to open source
https://github.blog/2020-01-22-browse-good-first-issues-to-start-contributing-to-open-source/

- In case, you add a value to `CUSTOM_TXT` such as
    ```
    "CUSTOM_TXT": "Checkout this new post from The GitHub Blog"
    ```
    - The sample template for a post will be(*The GitHub Blog is name of the site*):

> Checkout this new post from The GitHub Blog
Browse good first issues to start contributing to open source
https://github.blog/2020-01-22-browse-good-first-issues-to-start-contributing-to-open-source/

- Initially, to add the entries that are already present on your website, run
```sh
python -m social_bost_pot.feeds.processor
```
This will add the links to the database.

- Try adding a post to your website(anyhow just add an item to your RSS feed) and test if everything is working well by running
```sh
python -m social_post_bot
```
If everything went well, you will get a message on telegram from your telegram bot about the response after posting.(I don't know if this is best way to notify the owner about the posting but currently, it is as it is.)

- Now schedule a [`cron`](https://en.wikipedia.org/wiki/Cron) job for running the script `python -m social_post_bot` according to your requirements.

TODO
- Support LinkedIn.
- Use hashtags when posting content to sites like twitter, facebook etc with tags if provided.
