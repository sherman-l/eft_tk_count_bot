dictionary = {}

### Error Strings ###
dictionary['tk_invalid_params'] = '引数の数が間違っています！　正しい使い方は: ```$tk @殺し屋 @殺された人``` 殺し屋と殺された人は同じ人にするのはダメです'
dictionary['stats_invalid_params'] = '使い方が間違っています! 正しい使い方は: ```$stats @探したいユーザー``` このサーバー中の全員の情報を探したいなら: ```$stats```'
dictionary['log_invalid_params'] = '使い方が間違っています! 正しい使い方は: ```$log #``` 「＃」は見たいキルログの数です。 ```$log``` だけを頼んだら一番最近のキルログ10個を見れます'
dictionary['lang_unrecognized_language'] = 'エラー！その言語は現在サポートしません！　現在サポートしてる言語：　```jp, en```'
dictionary['lang_insufficient_parameters'] = 'エラー！引数最低一つを入れてください！現在サポートしてる言語：　```jp, en```'
dictionary['unrecognized_command'] = 'コマンド分かりません。現在サポートしてる情報を欲しかったら「$help」を言ってください。'

### General Message Strings ###
dictionary['no_statistics_user'] = '{}様の情報がないです'
dictionary['no_statistics_server'] = 'このサーバーの情報がないです'
dictionary['kill_stats'] = 'ユーザー: {} \nチームキル数: {}'
dictionary['log_string'] = 'チーム殺し屋: {} \t 被害者: {} \t 年月日: {}'
dictionary['ranking_row'] = 'ランク: {} \t名前: {} \tチームキル数: {}'
dictionary['tk_rankings'] = 'チームキルのランキング'

### Success Strings ####
dictionary['tk_log_entry_success'] = '{} が {} 仲間を殺したログはデーターベースに入る事が成功しました！'
dictionary['lang_change_success'] = 'ボットの言語を日本語に変えました！'

### Embed Fields ###
dictionary['embed_kill_count'] = 'チームキル数'
dictionary['embed_stats_title'] = '{} チームキルリポート'
dictionary['stats_embed_footer'] = 'ユーザー {} / {}'

dictionary['help_message'] = """現在サポートしてるコマンド ()に入ってるは随意の引数です:
```
$tk ＠殺し屋　＠殺された人 ： チームキルログをデータベースに入れる事が出来ます。 \n
$stats (＠ユーザー) ：　ユーザーのチームキルリポートを見る事が出来ます。 \n
$log (#) : 一番最近のログ「＃」個を見ること。「＃」を言わなかったら一番最近の10個を見る事が出来ます。\n
$lang [en, jp] : このボットの言語を変えれます。現在サポートしてる言語は英語と日本語です。\n
$rank : サーバーのユーザーのチームキルランキングを見る事が出来ます。\n
$help : ヘルプメッセージを見る事が出来ます。
```
"""
