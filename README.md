<h1>MIRC Data Dashboard</h1>
<p>
Measuring Internet Resilience in the Caribbean (MIRC) Data Dashboard is an open-source project that was created to supplement a <a href="https://myuwi-my.sharepoint.com/:b:/g/personal/tyler_seudath_my_uwi_edu/EczggQZVOvlMnLF5Mv6LUWkBpj-vyp9R2FnIreAEZyreyA?e=QDfXW9">guide book</a> on the deployment of a self-hosted Measurement Lab (<a href="https://www.measurementlab.net/">M-Lab</a>) Network Diagnostic Tool (<a href="https://www.measurementlab.net/tests/ndt/">NDT</a>) server that writes all internet measurements to a Dropbox cloud storage. 
</p>

<h2>Prerequisites</h2>
<p>The following prerequisites must be satisfied before this project can be used:</p>
  <ol>
  <li>An NDT server must be deployed and must write all internet measurements to a Dropbox Cloud storage as described in the <a href="https://myuwi-my.sharepoint.com/:b:/g/personal/tyler_seudath_my_uwi_edu/EczggQZVOvlMnLF5Mv6LUWkBpj-vyp9R2FnIreAEZyreyA?e=QDfXW9">guide book</a></li>
  <li>A SendGrid account and API token must be generated <a href="https://myuwi-my.sharepoint.com/:b:/g/personal/tyler_seudath_my_uwi_edu/EczggQZVOvlMnLF5Mv6LUWkBpj-vyp9R2FnIreAEZyreyA?e=QDfXW9">(See guide book)</a></li>
  <li>A Dropbox refresh token must be created for the Dropbox Cloud storage <a href="https://myuwi-my.sharepoint.com/:b:/g/personal/tyler_seudath_my_uwi_edu/EczggQZVOvlMnLF5Mv6LUWkBpj-vyp9R2FnIreAEZyreyA?e=QDfXW9">(See guide book)</a></li>
  <li>Python 3.9 must be installed</li>
  </ol>

<h2>Installation and Configuration</h2>
<p>The following steps describe the installation and configuration of the project onto a local machine:</p>
<ol>
<li>Clone the repository onto a local machine</li>
<li>With a Python interpreter, navigate to the project's root directory (MIRC-Data-Dashboard) and install the project's dependencies from <a href="https://github.com/MIRC-Project/MIRC-Data-Dashboard/blob/ffd1a545d834ba12e3c49382b8a7497c051b55c4/requirements.txt">/requirements.txt</a> with pip<br><code>pip install -r requirements.txt</code></li>
<li>Create a Database Migration Repository</li>
  <ol>
  <li>Navigate to the project's root directory with the Python interpreter</li>
  <li>Initialize the migration repository:<br><code>flask db init</code></li>
  <li>Create a migration script that will contain the current database models of the project<br><code>flask db migrate</code></li>
  <li>Commit the migration script to add the models to the database<br><code>flask db commit</code></li>
  <li>Any future changes made to the database's structure in <a href="https://github.com/MIRC-Project/MIRC-Data-Dashboard/blob/ffd1a545d834ba12e3c49382b8a7497c051b55c4/app/models.py">/app/models.py</a> must be added to the database with <code>flask db migrate</code> and <code>flask db upgrade</code></li>
  </ol>
<li>Add the following environmental variables as generated in the <a href="https://myuwi-my.sharepoint.com/:b:/g/personal/tyler_seudath_my_uwi_edu/EczggQZVOvlMnLF5Mv6LUWkBpj-vyp9R2FnIreAEZyreyA?e=QDfXW9">guide book</a> to <a href="https://github.com/MIRC-Project/MIRC-Data-Dashboard/blob/ffd1a545d834ba12e3c49382b8a7497c051b55c4/config.py">/config.py</a>:</li>
  <ul>
  <li><code>MAIL_PASSWORD</code> - SendGrid API Token</li>
  <li><code>MAIL_DEFAULT_SENDER</code> - SendGrid Email Address</li>
  <li><code>APP_KEY</code> - Dropbox Account App Key</li>
  <li><code>APP_SECRET</code> - Dropbox Account App Secret</li>
  <li><code>OAUTH2_REFRESH_TOKEN</code> - Dropbox Account Refresh Token</li>
  </ul>
</ol>

<h2>Usage</h2>
<p>Select the environment that contains the project's dependencies with a Python interpreter. In the interpreter, Navigate to the project's root directory and enter <code>python main.py</code> to run the project. The project's session can be terminated with <code>CTRL + c</code> keyboard shortcut.</p>
<p>The data dashboard can be accessed at <a href="http://localhost:5000">localhost:5000</a> or <a href="http://127.0.0.1:5000">127.0.0.1:5000</a>.</p>
