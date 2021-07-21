dictionary = {}

### Error Strings ###
dictionary['tk_invalid_params'] = 'Invalid number of params! \nAppropriate usage: ```$tk @killer @killed``` Killer must also not be same as killed'
dictionary['stats_invalid_params'] = 'Incorrect usage! Correct usage: ```$stats @user``` Or alternatively to see all stats: ```$stats```'
dictionary['log_invalid_params'] = 'Incorrect usage! Correct usage: ```$log #``` where # is any number representing number of logs you wish to see, or ```$log``` to see the last 10 logs by default'
dictionary['lang_unrecognized_language'] = 'Unable to recognize language or unsupported language! Currently supported languages: ```jp, en```'
dictionary['lang_insufficient_parameters'] = 'Please enter at least one parameter! Currently supported languages: ```jp, en```'
dictionary['unrecognized_command'] = 'Unrecognized command! Available commands can be found by saying $help'

### General Message Strings ###
dictionary['no_statistics_user'] = 'No stats available for {}'
dictionary['no_statistics_server'] = 'No stats available for server'
dictionary['kill_stats'] = 'User: {} \nTeam Kills: {}'
dictionary['log_string'] = 'Team Killer: {} \t Victim: {} \t Date: {}'
dictionary['ranking_row'] = 'Rank: {} \tName: {} \tKill Count: {}'
dictionary['tk_rankings'] = 'TK Rankings'

### Success Strings ####
dictionary['tk_log_entry_success'] = '{} team killing {} log entered successfully!'
dictionary['lang_change_success'] = 'Language changed successfully to English!'

### Embed Fields ###
dictionary['embed_kill_count'] = 'Team Kill Count'
dictionary['embed_stats_title'] = '{} tk stats'
dictionary['stats_embed_footer']= 'User {} out of {}'

dictionary['help_message'] = """Currently supported commands. Parameters encased in () are optional:
```
$tk @killer　@killed ： Record a team kill into the database  \n
$stats (@user) ：　Displays the current team kill stats of a user \n
$log (#) : Displays the most recent (#) of team kill entries. Defaults to 10 if unspecified. \n
$lang [en, jp] : Changes the language of the messages for this bot. Currently only supports English and Japanese. \n
$rank : Displays the team kill rankings for the users of this server. \n
$help : Displays this help message.
```
"""
