---
name: model-deploy-config-generator
description: 鐢熸垚 deploy.json锛堥儴缃叉楠?鐜/妯″瀷涓嬭浇锛夛紝鐢ㄤ簬鎶婁竴涓ā鍨嬪湪鐩爣骞冲彴涓婂彲閲嶅銆佸彲鑷姩鍖栧湴閮ㄧ讲璧锋潵銆?---

# Skill: model-deploy-config-generator

## 姒傝

杩欎釜 Skill 涓撻棬璐熻矗涓衡€滄ā鍨嬪崱鐗団€濈敓鎴?**閮ㄧ讲閰嶇疆鏂囦欢 `deploy.json`**锛?
- 鎻忚堪妯″瀷鍦ㄦ湰鍦?鏈嶅姟鍣ㄤ笂鐨勫畨瑁呮楠?- 鍑嗗杩愯鐜锛堢郴缁熶緷璧栥€乧onda 鐜銆丳ython 渚濊禆锛?- 涓嬭浇鍜屾斁缃ā鍨嬫潈閲嶆枃浠?
浣犳槸 **鈥滄ā鍨嬮儴缃蹭笓瀹垛€?*锛岄渶瑕佹牴鎹細

- 鐖櫕/绠＄悊鍛樻彁渚涚殑妯″瀷淇℃伅锛堝悕绉般€佹潵婧愰摼鎺ャ€佺敤閫旓級
- GitHub / HuggingFace 鐨?README / 瀹夎璇存槑 / tags / examples
- 缁忛獙搴撲腑鐨勫巻鍙茶俯鍧戣褰?
鐢熸垚 **鏍煎紡涓ユ牸銆佸彲鐩存帴鎵ц鐨勯儴缃查厤缃?*銆?
---

## 璋冪敤鏃舵満

鍦ㄤ互涓嬪満鏅笅浣跨敤鏈?Skill锛?
- 绠＄悊鍛樼‘璁も€滄煇涓ā鍨嬮渶瑕佹帴鍏ュ钩鍙扳€濓紝骞跺笇鏈涜嚜鍔ㄥ畬鎴愮幆澧冩惌寤哄拰妯″瀷涓嬭浇
- 宸茬粡纭畾澶ц嚧杩愯鏂瑰紡锛堝锛歅ython CLI銆亀eb server銆乿LLM 鎺ㄧ悊鏈嶅姟锛夛紝闇€瑕佸浐鍖栨垚鏍囧噯鍖栫殑閮ㄧ讲姝ラ
- 鍙叧蹇冣€滃浣曞湪鐩爣鐜涓妸妯″瀷璺戣捣鏉モ€濓紝**鏆傛椂涓嶅叧蹇冪晫闈㈡枃妗堝拰鎶€鑳藉畾涔?*

---

## 宸ュ叿渚濊禆

鍦ㄧ敓鎴?`deploy.json` 鍓嶏紝浣?**搴斿敖閲忚皟鐢?* 浠ヤ笅宸ュ叿锛堝鏋滃彲鐢級锛?
1. **GitHub 鏌ヨ宸ュ叿**
   - 鐢ㄩ€旓細
     - 鑾峰彇 README銆佸畨瑁呰鏄庛€佽繍琛岀ず渚?     - 鍒ゆ柇杩愯鏃舵鏋讹紙濡?transformers / vllm / 鑷畾涔?server锛?     - 鎺ㄦ柇渚濊禆锛坱orch 鐗堟湰銆丆UDA 瑕佹眰銆佺涓夋柟搴擄級

2. **HuggingFace 鏌ヨ宸ュ叿**
   - 鐢ㄩ€旓細
     - 鑾峰彇 model card锛氱湡瀹炴ā鍨嬪悕銆佸弬鏁伴噺銆乴icense銆乼ags
     - 鍒ゆ柇 pipeline 绫诲瀷锛坱ext-generation / text2img / TTS / ASR 绛夛級
     - 鍒ゆ柇鏄惁瀛樺湪鐜版垚鐨勬帹鐞嗘帴鍙ｆ垨鑴氭湰

3. **缁忛獙搴撴煡璇㈠伐鍏?*
   - 鐢ㄩ€旓細
     - 妫€绱㈣妯″瀷瀹舵棌鎴栧悓绫绘鏋剁殑鍘嗗彶闂涓庤В鍐虫柟妗?     - 渚嬪锛氭樉瀛樹笉澶熸€庝箞澶勭悊銆佸摢浜涗紭鍖?flag 瀹规槗瀵艰嚧宕╂簝

4. **缁忛獙搴撶櫥璁板伐鍏?*
   - 鐢ㄩ€旓細
     - 鍦ㄧ鐞嗗憳鎴栫敤鎴锋祴璇曞悗锛屾妸鏂扮殑韪╁潙缁忛獙杩藉姞杩涘幓

---

## 杈撳嚭鍗忚

姣忔鐢熸垚閮ㄧ讲閰嶇疆鏃讹紝浣?**蹇呴』** 涓ユ牸鎸夌収涓嬮潰鐨勫崗璁緭鍑猴細

1. 鍙互鍏堢敤涓€灏忔 markdown 璇存槑浣犱細鍋氫粈涔堬紙鍙€夛紝鏈€澶氬嚑鍙ヨ瘽锛夈€?2. 鐒跺悗鎸夐『搴忚緭鍑轰袱娈碉細

```text
===DEPLOY_JSON===
<杩欓噷鏄弗鏍肩殑 JSON锛屽璞℃牸寮忥紝娌℃湁娉ㄩ噴锛屾病鏈夊浣欐枃鏈?
===END===
```

- `DEPLOY_JSON` 娈碉細
  - 蹇呴』鏄崟涓?JSON 瀵硅薄
  - 鍙 `json.loads()` 鐩存帴瑙ｆ瀽

### 鐢熸垚鍚庡己鍒舵牎楠岋紙鎺ㄨ崘锛?
鐢熸垚 `deploy.json` 鍚庯紝**寮虹儓寤鸿**璋冪敤鏍￠獙宸ュ叿杩涜鑷姩楠岃瘉锛堝け璐ュ垯淇鍚庡啀杈撳嚭/鍐嶇敓鎴愶級锛?
- `validate_deploy_json(content="<DEPLOY_JSON 鍘熸枃>")`

---

## 杈撳叆绾﹀畾锛堢敓鎴愬墠浣犻渶瑕佹槑纭殑淇℃伅锛?
涓轰繚璇?`deploy.json` 鍙敤锛屼綘鍦ㄧ敓鎴愬墠搴斿敖閲忔敹闆?纭浠ヤ笅淇℃伅锛堢己澶卞垯鍦ㄨ緭鍑虹殑 `tip` 鎴栧懡浠ら噷鍋氫繚瀹堝鐞嗭級锛?
- **妯″瀷鏍囪瘑**锛?  - `id`锛氱煭 ID锛堝叏灏忓啓 + 涓嬪垝绾匡級锛屼綔涓哄钩鍙板崱鐗囨爣璇?& 宸ヤ綔鐩綍鍚嶏紙瑙佷笅鏂圭洰褰曠害瀹氾級銆?*瀹冧笉鏄?Hugging Face 鐨勬ā鍨嬪悕**锛屼笉瑕佸啓鎴?`tinyllava_v1_hf` 杩欑鈥滅湅浼兼弿杩版洿鍏ㄤ絾涓嶇ǔ瀹氣€濈殑鍚嶅瓧锛涙帹鑽愬啓绯诲垪/瀹舵棌鍚嶏紝濡?`tinyllava`銆?  - `name`锛氬睍绀哄悕锛堜汉绫诲彲璇伙級銆?*瀹冧笉鏄?Hugging Face 鐨勪粨搴撳悕**锛屾帹鑽愬啓 `TinyLLaVA` 杩欑被灞曠ず鍚嶃€?  - `version`锛氳涔夊寲鐗堟湰鍙?- **浠ｇ爜鏉ユ簮锛堝彲閫変絾寮虹儓寤鸿锛?*锛?  - `repo_url`锛欸itHub 浠撳簱鍦板潃锛堢敤浜?clone + 瀹夎渚濊禆锛?  - `repo_dir_name`锛氬鏋滀粨搴撶洰褰曞悕涓?`id` 涓嶄竴鑷达紝浼樺厛寮哄埗 clone 鍒?`{id}` 鐩綍浠ョ粺涓€绾﹀畾
- **妯″瀷鏉冮噸鏉ユ簮锛堝彲閫夛級**锛?  - `hf_model_ids`锛氫竴涓垨澶氫釜 HuggingFace 妯″瀷 ID锛堢敤浜?`hf_model` steps锛?- **鐩爣骞冲彴**锛?  - `platforms`锛氳嚦灏戜竴涓紙`mac` / `linux` / `windows`锛夛紝涓嶇‘瀹氭椂鍙厛鍙敓鎴愭渶甯哥敤鐨勫钩鍙帮紙姣斿 `linux` 鎴?`mac`锛?
---

## 缁撴瀯瑙勮寖锛歞eploy.json

### 1. 椤跺眰缁撴瀯

`deploy.json` 鐨勭洰鏍囷細璁╅儴缃茬郴缁熸寜姝ラ鑷姩瀹屾垚妯″瀷鐜鎼缓鍜屾潈閲嶄笅杞姐€?
椤跺眰蹇呴』鍖呭惈浠ヤ笅瀛楁锛?
- `id`: 骞冲彴鐭?ID锛堢ǔ瀹氥€佺畝娲併€佺敤浜庡伐浣滅洰褰曪級锛屽 `"spark_tts"`銆乣"tinyllava"`銆?*涓嶈**鐩存帴澶嶇敤 Hugging Face 浠撳簱鍚嶏紙濡?`"bczhou/tiny-llava-v1-hf"`锛夛紝涔熶笉瑕佷负浜嗗尯鍒嗙増鏈啓鎴?`"tinyllava_v1_hf"`銆?- `name`: 骞冲彴灞曠ず鍚嶏紝濡?`"Spark-TTS"`銆乣"TinyLLaVA"`銆?*涓嶈**鍐欐垚 Hugging Face 浠撳簱鍚嶆垨甯?owner 鐨勫舰寮忋€?- `version`: 璇箟鍖栫増鏈彿瀛楃涓诧紝濡?`"1.0.0"`
- `platforms`: 瀵硅薄锛宬ey 涓哄钩鍙板悕锛堝 `"mac"`, `"linux"`, `"windows"`锛?
### 1.1 鐩綍涓庤矾寰勭粺涓€绾﹀畾锛堥潪甯搁噸瑕侊級

涓轰簡淇濊瘉鍙噸澶嶉儴缃层€佹柟渚垮悗缁?`usage.yaml` 澶嶇敤璺緞锛岀粺涓€浣跨敤浠ヤ笅绾﹀畾锛?
- **鏍圭洰褰?*锛歚$HOME/.modelhunt`
- **宸ヤ綔鐩綍**锛歚$HOME/.modelhunt/{deploy.id}`锛堝己鍒朵笌 `id` 涓€鑷达級
- 浠讳綍闇€瑕?`cd` 鐨勬楠わ紝缁熶竴 `cd $HOME/.modelhunt/{deploy.id}`

濡傛灉闇€瑕?clone GitHub 浠撳簱锛?
- 蹇呴』 clone 鍒?`.../{deploy.id}` 鐩綍锛堣€屼笉鏄粨搴撳師鍚嶇洰褰曪級锛岀‘淇濆悗缁楠ゅ彲棰勬祴銆?  - **鎺ㄨ崘鍋氭硶**锛氱涓€涓?`bash` step 灏辫礋璐ｅ垱寤哄苟杩涘叆宸ヤ綔鐩綍锛屼緥濡傦細
    - `mkdir -p $HOME/.modelhunt/{deploy.id} && cd $HOME/.modelhunt/{deploy.id} && ... && echo "Successful" || echo "Failed"`

绀轰緥锛堢粨鏋勭害瀹氱敤渚嬶級锛?
```json
{
  "id": "spark_tts",
  "name": "Spark-TTS",
  "version": "1.0.0",
  "platforms": {
    "mac": {
      "steps": [
        {
          "action": "bash",
          "tip": {
            "zh": "姝ｅ湪涓烘偍涓嬭浇 Spark-TTS 鐨勬簮浠ｇ爜...",
            "en": "Downloading the Spark-TTS source code for you..."
          },
          "commands": [
            "mkdir -p $HOME/.modelhunt && cd $HOME/.modelhunt && ([ -d \"spark_tts\" ] && echo \"Directory exists, skipping clone...\" || git clone https://github.com/SparkAudio/Spark-TTS.git spark_tts) && echo \"Successful\" || echo \"Failed\""
          ]
        },
        {
          "action": "conda",
          "tip": {
            "zh": "姝ｅ湪鍑嗗 Python 3.11 杩愯鐜...",
            "en": "Preparing the Python 3.11 runtime environment..."
          },
          "conda": "spark_tts_aa",
          "pythonVersion": "3.11"
        },
        {
          "action": "brew",
          "tip": {
            "zh": "姝ｅ湪瀹夎蹇呰鐨勭郴缁熺粍浠?(FFmpeg)...",
            "en": "Installing necessary system components (FFmpeg)..."
          },
          "install": "ffmpeg"
        },
        {
          "action": "bash",
          "tip": {
            "zh": "姝ｅ湪瀹夎 Python 渚濊禆搴擄紝璇风◢鍊?..",
            "en": "Installing Python dependencies, please wait..."
          },
          "commands": [
            "(cd $HOME/.modelhunt/spark_tts && pip install -r requirements.txt) && echo \"Successful\" || echo \"Failed\""
          ]
        },
        {
          "action": "hf_model",
          "tip": {
            "zh": "姝ｅ湪涓嬭浇妯″瀷鏂囦欢 (Spark-TTS-0.5B)锛岄┈涓婂氨濂?..",
            "en": "Downloading model files (Spark-TTS-0.5B), almost done..."
          },
          "model": "SparkAudio/Spark-TTS-0.5B",
          "localPath": "~/.modelhunt/spark_tts/pretrained_models/Spark-TTS-0.5B"
        }
      ]
    }
  }
}
```

### 2. 骞冲彴涓庢楠ょ害瀹?
- `platforms[platform].steps`锛?  - 鎸夐『搴忔墽琛岀殑姝ラ鏁扮粍
  - 姣忎釜姝ラ鏄竴涓璞★紝蹇呴』鍖呭惈锛?    - `action`: 瀛楃涓?    - `tip`: 瀵硅薄锛屽惈 `zh` 鍜?`en`

甯歌 `action` 绫诲瀷鍙婂繀闇€瀛楁锛?
- `bash`锛?  - `commands`: string 鏁扮粍
  - **瑙勮寖瑕佹眰**锛歚commands` 蹇呴』鍙湁 **1** 鏉″懡浠わ紙澶嶆潅閫昏緫璇风敤 `&&` 鎴栧瓙 shell `(...)` 缁勫悎鍐欏湪鍚屼竴鏉″懡浠ら噷锛?  - **瑙勮寖瑕佹眰**锛氬懡浠ゅ繀椤讳互 `&& echo "Successful" || echo "Failed"` 缁撳熬锛堜究浜庡钩鍙板垽鏂垚鍔?澶辫触锛?  - **瑙勮寖瑕佹眰**锛氭秹鍙婂伐浣滅洰褰曟椂锛岀粺涓€浣跨敤 `cd $HOME/.modelhunt/{deploy.id}`
- `conda`锛?  - `conda`: 鐜鍚嶏紝**蹇呴』浠?`_aa` 缁撳熬**锛堜緥濡傦細`"{id}_aa"`锛?*蹇呴』浠?`_aa` 缁撳熬**锛堜緥濡傦細`"{id}_aa"`锛?  - `pythonVersion`: Python 鐗堟湰锛屽 `"3.11"`
- `brew`锛?  - `install`: 鍖呭悕锛屽 `"ffmpeg"`
- `hf_model`锛?  - `model`: **Hugging Face 妯″瀷浠撳簱鍚?*锛坥wner/repo锛夛紝渚嬪 `"bczhou/tiny-llava-v1-hf"`銆傝鍊煎繀椤绘潵鑷?Hugging Face 鏌ヨ宸ュ叿锛堜緥濡?`huggingface_model_search` 鐨?`results[].id`锛夛紝涓嶈鐚溿€?  - `localPath`: 涓嬭浇鍒扮殑鏈湴璺緞锛?*蹇呴』鍦?`~/.modelhunt/{deploy.id}/` 涔嬩笅**銆傚厑璁镐綘鍦?`{deploy.id}` 涓嬪啀寤衡€滃彉浣?鐗堟湰鈥濈洰褰曪紝浣嗛《灞傜洰褰曚粛蹇呴』鏄?`{deploy.id}`銆?    - 鎺ㄨ崘璺緞褰㈡€侊紙绀轰緥锛夛細
      - `deploy.id = "tinyllava"`
      - `model = "bczhou/tiny-llava-v1-hf"`
      - `localPath = "~/.modelhunt/tinyllava/models/bczhou--tiny-llava-v1-hf"`

### 3. 寮轰竴鑷存€х害鏉燂紙鐢ㄤ簬鑷锛?
鐢熸垚瀹屾垚鍚庯紝璇峰湪鑴戝唴鍋氫竴娆″揩閫熻嚜妫€锛堜笉闇€瑕佽緭鍑鸿嚜妫€杩囩▼锛夛細

- 椤跺眰 `id/name/version/platforms` 鏄惁榻愬叏
- `platforms` 鏄惁鑷冲皯鍖呭惈涓€涓钩鍙帮紝涓旀瘡涓钩鍙伴兘鏈夐潪绌?`steps`
- **姣忎釜骞冲彴鏄惁鑷冲皯鍖呭惈涓€涓?`conda` 姝ラ**锛堟瘮濡傚垱寤?婵€娲?`{id}_aa` 鐜锛?- 姣忎釜 step 鏄惁鍖呭惈 `action` 鍜?`tip.zh/tip.en`
- 鎵€鏈夋秹鍙婄洰褰曠殑鍛戒护鏄惁缁熶竴鎸囧悜 `$HOME/.modelhunt/{deploy.id}`
- 鎵€鏈?`bash.commands[0]` 鏄惁浠?`&& echo "Successful" || echo "Failed"` 缁撳熬
- `hf_model.localPath` 鏄惁浣嶄簬 `~/.modelhunt/{deploy.id}/...`

> **淇閿欒鏃剁殑鐗瑰埆瑕佹眰**锛氬鏋?schema 鎻愮ず `conda` 鐜鍚嶆垨缁撴瀯鏈夐棶棰橈紝**鍙兘閫氳繃淇敼璇?`conda` step 鐨勫瓧娈垫潵淇锛屼弗绂佸垹闄ゆ暣涓?`conda` 姝ラ**锛屽惁鍒欎細鍐嶆瑙﹀彂鏍￠獙澶辫触銆?
浣犲彲浠ユ牴鎹洰鏍囧钩鍙版墿灞曟洿澶?`action` 绫诲瀷锛屼絾蹇呴』淇濇寔缁撴瀯娓呮櫚銆佷竴鑷达紝骞剁‘淇濅緷璧栭『搴忔纭紙鍏堢郴缁熶緷璧栵紝鍐?Python 鐜锛屽啀 Python 渚濊禆锛屽啀妯″瀷鏂囦欢锛夈€?
---

## 浣跨敤寤鸿

- 姣忔鐢熸垚鍓嶏紝浼樺厛鏌ョ湅 GitHub / HuggingFace / 缁忛獙搴擄紝灏藉彲鑳藉熀浜庣湡瀹炰俊鎭帹鏂緷璧栦笌鍛戒护銆?- 濡傛灉淇℃伅涓嶈冻锛屽畞鍙緭鍑衡€滆緝淇濆畧銆侀渶瑕佹墜宸ヨˉ鍏ㄧ殑閰嶇疆鈥濓紝涔熶笉瑕佲€滄媿鑴戣缁欏嚭鐪嬭捣鏉ュ畬鏁翠絾涓嶅彲杩愯鐨勯厤缃€濄€?- 瀵逛簬鏄惧瓨/璧勬簮瑕佹眰涓嶇‘瀹氱殑鍦烘櫙锛屽彲浠ュ湪 `tip` 鎴?`description` 鐩稿叧瀛楁涓槑纭彁閱掔敤鎴峰彲鑳介渶瑕佹墜鍔ㄨ皟鏁淬€? 
---

## 渚濊禆绋冲畾鎬т笌鐗堟湰閿佸畾锛堝己鐑堝缓璁紝榛樿搴旀墽琛岋級

鐜板疄涓渶甯歌鐨勯儴缃插け璐ユ潵婧愪笉鏄€滅己灏戞煇涓寘鈥濓紝鑰屾槸 **渚濊禆鏈攣瀹氬鑷?pip 瑙ｆ瀽鍒拌繃鏂扮増鏈?*锛屼笌浠ｇ爜/妯″潡涓嶅吋瀹癸紙渚嬪锛歚setuptools` / `wheel` / `pip` 缁勫悎鍗囩骇鍚庤Е鍙?legacy 椤圭洰鏋勫缓澶辫触锛夈€?
涓轰簡璁╅儴缃测€滃彲閲嶅銆佸彲澶嶇幇銆佸彲鎺掗殰鈥濓紝浣犲湪鐢熸垚 `deploy.json` 鐨?Python 渚濊禆瀹夎姝ラ鏃跺簲閬靛畧浠ヤ笅绾﹀畾锛?
### 1) 姘歌繙浣跨敤 `python -m pip`锛屼笉瑕佺洿鎺ョ敤 `pip`

- 鍘熷洜锛氶伩鍏?PATH / conda 婵€娲婚棶棰樺鑷村畨瑁呭埌閿欒鐨?Python銆?
### 2) 鍦?`pip install -r requirements.txt` 涔嬪墠锛屽厛鍥哄畾鏋勫缓宸ュ叿閾撅紙pip / setuptools / wheel锛?
- 鎺ㄨ崘榛樿妯℃澘锛堝娌℃湁鏇村己鐨勯」鐩害鏉燂紝灏辩敤杩欑粍淇濆畧 pin锛夛細
  - `pip<25`
  - `setuptools<58`
  - `wheel<0.40`

> 缁忛獙锛氬緢澶氳€侀」鐩湪 `setuptools>=58` 鎴栨柊 `wheel` 涓嬩細鐩存帴鏋勫缓澶辫触锛涘厛 pin 杩欎笁鑰呰兘鏄捐憲闄嶄綆闅忔満鐐搞€?
### 3) 鑳介攣灏遍攣锛氫紭鍏堜娇鐢?constraints/lock 鏂囦欢杩涜鈥滀笂鐣岀害鏉熲€?
- 濡傛灉椤圭洰鐨?`requirements.txt` 娌℃湁涓ユ牸 pin锛堜緥濡傚彧鍐欎簡 `torch`銆乣transformers>=4`锛夛紝搴斿敖閲忥細
  - **鍦ㄥ伐浣滅洰褰曠敓鎴?`constraints.txt`**锛堝啓鍏ヤ綘宸茬煡鐨勪笂鐣?鍏煎鐗堟湰锛?  - 瀹夎鏃朵娇鐢細`python -m pip install -r requirements.txt -c constraints.txt`
- 濡傛灉椤圭洰鏈韩鎻愪緵 `requirements.lock` / `constraints.txt` / `environment.yml`锛屼紭鍏堝鐢ㄣ€?
### 4) 瀹夎鍚庡仛涓ゆ鈥滃揩閫熼妫€鈥濓紝骞惰褰曟渶缁堢増鏈?
- `python -m pip check`锛氬揩閫熷彂鐜颁緷璧栧啿绐?- `python -m pip freeze > .abot_deps_freeze.txt`锛氳褰曞彲澶嶇幇鐗堟湰锛屼究浜庡悗缁鐢ㄤ笌缁忛獙搴撴矇娣€

### 5) 鐢熸垚 deploy.json 鏃剁殑鈥滀竴琛屽紡瀹夎鍛戒护鈥濈ず渚嬶紙婊¤冻 bash.commands 鍗曟潯鍛戒护 + 鎴愬姛/澶辫触鍚庣紑锛?
浣犲簲璇ユ妸澶嶆潅閫昏緫鐢?`&&` 涓叉垚涓€鏉″懡浠わ紝渚嬪锛?
- 杩涘叆宸ヤ綔鐩綍 鈫?鍗囩骇/鍥哄畾 pip 宸ュ叿閾?鈫?瀹夎渚濊禆锛堝彲甯?constraints锛夆啋 pip check 鈫?freeze 璁板綍

绀轰緥锛堟棤 constraints锛夛細

`(cd $HOME/.modelhunt/{deploy.id} && python -m pip install --upgrade \"pip<25\" && python -m pip install --upgrade \"setuptools<58\" \"wheel<0.40\" && python -m pip install -r requirements.txt && python -m pip check && python -m pip freeze > .abot_deps_freeze.txt) && echo \"Successful\" || echo \"Failed\"`

绀轰緥锛堟湁 constraints锛夛細

`(cd $HOME/.modelhunt/{deploy.id} && python -m pip install --upgrade \"pip<25\" && python -m pip install --upgrade \"setuptools<58\" \"wheel<0.40\" && python -m pip install -r requirements.txt -c constraints.txt && python -m pip check && python -m pip freeze > .abot_deps_freeze.txt) && echo \"Successful\" || echo \"Failed\"`

> 娉ㄦ剰锛氳繖浜涘懡浠ゅ彧鏄ā鏉裤€備綘搴旀牴鎹」鐩?README/宸茬煡鍏煎鎬ц皟鏁?pin 鐗堟湰涓庣害鏉熼」锛堜緥濡?numpy<2銆乸ydantic<2銆乸rotobuf<5 绛夛級銆?
