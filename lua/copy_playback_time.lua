function copy_time()
    local pos = mp.get_property_number("time-pos")
    if pos then
      local ms = string.format("%.3f", pos * 1000)
      os.execute("echo '" .. ms .. "' | pbcopy")
      mp.osd_message("⏱ Copied: " .. ms .. " ms", 1)
    end
  end
  
  mp.add_key_binding("t", "copy-time", copy_time)