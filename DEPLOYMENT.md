# How to deploy

---

## gcloud によるデプロイ基本事項

```bash
gcloud functions deploy NAME --entry-point NAME --runtime RUNTIME TRIGGER [FLAGS...]
```

> note
> `--entry-point`オプションは、デプロイする関数の名前が規約を満たしていない場合や関数名とエントリポイント名を変えたい場合に設定するもの

## Deployment of `search_queue`

```bash
gcloud functions deploy user_search_queue \
--runtime python37 \
--trigger-http \
--set-env-vars "SLACK_SECRET=[YOUR_SLACK_SIGNING_SECRET]" \
--allow-unauthenticated \
--project [PROJECT_ID]
```

> `--allow-unauthenticated`: 認証不要フラグ
> 簡単のためCloudFunctionsのエントリポイントにどこからでもアクセスできるようにしている（公式チュートリアルに従った）が、
> より安全な状態にするならば、CloudFunctionsへのアクセスはVPC内のみ許可として、APIゲートウェイなどを立てるのが望ましい

## Deployment of `search_response`

```bash
gcloud functions deploy user_search_response \
--runtime python37 \
--trigger-topic user_search \
--set-env-vars "SLACK_SECRET=[YOUR_SLACK_SIGNING_SECRET]" \
--project [PROJECT_ID]
```

---

## References

See:

- [gcloud functions deploy | Google Cloud SDK Reference](https://cloud.google.com/sdk/gcloud/reference/functions/deploy)
- [Cloud Functions Deploying | Google Cloud Guide](https://cloud.google.com/functions/docs/deploying)
- [Cloud Functions Testing | Google Cloud Guide](https://cloud.google.com/functions/docs/testing/test-overview)
