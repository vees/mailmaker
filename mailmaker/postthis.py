import wordpresslib

url = ""

wp = wordpresslib.WordPressClient(url, '', '')

wp.selectBlog(0)

post = wordpresslib.WordPressPost()

post.title = 'Title'
post.description = 'Content'
#post.tags = ["wordpress", "lib", "python"]

# Set to False to save as a draft
idPost = wp.newPost(post, True)
