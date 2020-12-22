import markdown
f = open('./app/templates/about_body.md','r')
html = markdown.markdown(f.read())
out = open('./app/templates/about_body.html','w')
out.write(html)