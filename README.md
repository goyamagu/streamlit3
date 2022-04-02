## Summary
### YahooAPIを使って、地図表示＆降水予報するWebAppをStreamlitで実装。Streamlit Sharingでデプロイ。
## Reference
- https://cloud5.jp/yahooapi_lesson/#0-yahoo-japan-web-id-
- https://github.com/randyzwitch/streamlit-folium
## Note
- YahooのAPIキーをStreamlit Sharingで使いたかったので、StreamlitのSecrets管理機能を使用  
https://docs.streamlit.io/streamlit-cloud/get-started/deploy-an-app/connect-to-data-sources/secrets-management
- デプロイ時、NameError: name 'folium_static' is not defined streamlit　エラーが発生。最後はsetup.pyをpushすることで、解消。refのgithub参照。
