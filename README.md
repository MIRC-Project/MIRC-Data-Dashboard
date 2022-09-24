<h1>Documentation In Progress ...</h1>

<ol>
<b><li>Prerequisites <a href="https://myuwi-my.sharepoint.com/:b:/g/personal/tyler_seudath_my_uwi_edu/EczggQZVOvlMnLF5Mv6LUWkBpj-vyp9R2FnIreAEZyreyA?e=QDfXW9">(See guide)</a></li></b>
  <ol>
  <li>Deployed NDT7 server linked to a Dropbox storage</li>
  <li>SendGrid account and API token</li>
  <li>Dropbox refresh token</li>
  </ol>
<b><li>Clone the Repository</li></b>
  <ol>
  <li>git clone ...</li>
  </ol>
<b><li>Install the Libraries</li></b>
  <ol>
  <li>pip ...</li>
  </ol>
<b><li>Create the Database File</li></b>
  <ol>
  <li>flask db init</li>
  <li>flask db migrate</li>
  <li>flask db commit</li>
  </ol>
<b><li>Add Configuration Variables</li></b>
  <ol>
  <li>Navigate to config.py and set environmental variable <a href="https://myuwi-my.sharepoint.com/:b:/g/personal/tyler_seudath_my_uwi_edu/EczggQZVOvlMnLF5Mv6LUWkBpj-vyp9R2FnIreAEZyreyA?e=QDfXW9">(See guide)</a> as follows:</li>
    <ul>
    <li>MAIL_PASSWORD to SendGrid's API token</li>
    <li>MAIL_DEFAULT_SENDER to SendGrid's email account</li>
    <li>APP_KEY to the Dropbox account's app key</li>
    <li>APP_SECRET to the Dropbox account's app secret key</li>
    <li>OAUTH2_REFRESH_TOKEN to the Dropbox account's refresh key</li>
    </ul>
  </ol>
<b><li>Run the Code</li></b>
  <ol>
  <li>Select python environment with installed libraries</li>
  <li>python main.py</li>
  <li>localhost:5000 or 127.0.0.1:5000</li>
  <li>Terminate with CTRL + C</li>
  </ol>
</ol>
