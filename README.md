# Bot Template

This a basic template for python bots to be built upon.

This uses the py-cord module, instead of the outdated discord.py module


# Config file

To get your bot up and running, you need to edit the `data/config.json` file. Use the table below for information about what to add for each option.

| Config Option   | Config Value                                                                                                                                                                                               |
|-----------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| token           | Visit [developer portal](https://discord.com/developers/applications), create a new application, or go to an existing one, click Bot, and Add Bot, then copy the token, and paste it into the config file, |
| admin_roles     | A list of role ids in your discord server, which should be able to use the admin features of the bot (eg. kick, ban). Separate with commas.                                                                |
| guild_ids       | A list of guild (server) ids that you want your bot to be usable in. Separate with commas.                                                                                                                 |
| open_cat        | The ID of the category for open tickets                                                                                                                                                                    |
| closed_cat      | The ID of the category for closed tickets                                                                                                                                                                  |
| welcome_channel | The ID of the channel to send member welcome messages to                                                                                                                                                   |
| total           | The ID of a voice channel to list the total number of members & bots in the server                                                                                                                         |
| bots            | The ID of a voice channel to list the total number of bots in the server                                                                                                                                   |
| members         | The ID of a voice channel to list the total number of members in the server                                                                                                                                |