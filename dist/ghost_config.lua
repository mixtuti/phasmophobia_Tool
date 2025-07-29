obs = obslua

-- 初期設定
settings = {
  columns = 3,
  font_size = 18,
  max_ghosts = 10,
  refresh_interval = 2,
  show_remaining = true
}

-- 保存先ファイル
config_filename = script_path() .. "config.json"

-- UIプロパティの定義
function script_properties()
  local props = obs.obs_properties_create()

  obs.obs_properties_add_int(props, "columns", "候補ゴーストの列数", 1, 10, 1)
  obs.obs_properties_add_int(props, "font_size", "フォントサイズ", 10, 60, 1)
  obs.obs_properties_add_int(props, "max_ghosts", "最大表示数", 1, 50, 1)
  obs.obs_properties_add_int(props, "refresh_interval", "更新間隔（秒）", 1, 60, 1)
  obs.obs_properties_add_bool(props, "show_remaining", "他◯種類の表示")

  return props
end

-- UIの更新時に呼ばれる
function script_update(settings_obj)
  settings.columns = obs.obs_data_get_int(settings_obj, "columns")
  settings.font_size = obs.obs_data_get_int(settings_obj, "font_size")
  settings.max_ghosts = obs.obs_data_get_int(settings_obj, "max_ghosts")
  settings.refresh_interval = obs.obs_data_get_int(settings_obj, "refresh_interval")
  settings.show_remaining = obs.obs_data_get_bool(settings_obj, "show_remaining")

  save_config()
end

-- JSONとして保存
function save_config()
  local json = string.format([[
{
  "font_size": %d,
  "columns": %d,
  "max_ghosts": %d,
  "refresh_interval": %d,
  "show_remaining": %s
}
]],
    settings.font_size,
    settings.columns,
    settings.max_ghosts,
    settings.refresh_interval,
    tostring(settings.show_remaining)
  )

  local file = io.open(config_filename, "w")
  if file then
    file:write(json)
    file:close()
    print("設定を保存しました: " .. config_filename)
  else
    print("設定ファイルを書き込めません: " .. config_filename)
  end
end

-- スクリプト説明
function script_description()
  return "Phasmophobia Ghost Overlay 設定\nconfig.json に保存され、HTMLで使用されます。"
end
