local fenced = "```%s\n%s\n```\n"

function CodeBlock(cb)
  return pandoc.RawBlock("markdown", fenced:format(cb.classes[1] or "", cb.text))
end
