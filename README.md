<img src="https://avatars2.githubusercontent.com/u/2810941?v=3&s=96" alt="Google Cloud Platform logo" title="Google Cloud Platform" align="right" height="96" width="96"/>

# User Search Slash Command with 2 Google Cloud Functions

---

## Cloud Functions Spec ~ `search_queue`

Features:

- Slashコマンドの受け口である（SlashコマンドのPOST先URLは本関数のエントリポイントとする）
- Slashコマンド（POSTリクエスト）によって起動するHTTPトリガー関数である
- Slashコマンドで渡されたリクエスト情報をCloud Pub/Subにパブリッシュする（トピックはuser_search）
- Slackに「処理中」の旨のレスポンスを返す


## Cloud Functions Spec ~ `search_response`

Features:

- `search_queue` 関数の `user_search` トピックのパブリッシュ処理によって起動するPub/Subトリガー関数である
- Slashコマンドの引数を解析し、[Mentaiko-API](https://github.com/data-learning-guild/portfolio-recommendation-api)にGETリクエストして、ユーザー検索処理をコールする
- Mentaiko-APIから返ってきたレスポンスを元に Slack Friendly なメッセージ（JSON）を生成し、Slashコマンドから受け取ったレスポンスURLにPOSTする

## Cloud Test (After Deploy)

### Trigger Functions From Slack

input command

```bash
# /user_search [KEY_WORD] [MAX_LIST_SIZE]
/user_search python 3
```

then, functions will respond like ...

```Markdown
Working on it! :dog2:
*python* に興味のあるユーザー一覧
> user0 (mention_to_user0) 0.98
> user4 (mention_to_user4) 0.76
> user1 (mention_to_user1) 0.34
```

### Debug

- Cloud Functions Dashboard.
- And then, See Logs.

---

## References

See:

* [Cloud Functions Slack tutorial][tutorial]
* [Cloud Functions Slack sample source code][code]
* [Slack Timeout Problem 解説記事 | Dev.to][article]
* [Slack Timeout Problem 解説記事のソース | GitHub][refcode]
* [Slack Message Formatting | Slack API Reference][slackmsgdoc]
* [Slack Block Kit Message Formatting Simulator][slackmsgsim]

[tutorial]: https://cloud.google.com/functions/docs/tutorials/slack
[doc]: https://cloud.google.com/functions/docs/writing
[code]: main.py
[article]: https://dev.to/googlecloud/getting-around-api-timeouts-with-cloud-functions-and-cloud-pub-sub-47o3
[refcode]: https://github.com/abbycar/doge-a-chat
[slackmsgdoc]: https://api.slack.com/reference/surfaces/formatting
[slackmsgsim]: https://app.slack.com/block-kit-builder
