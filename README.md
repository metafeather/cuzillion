# Overview

This repository attempts to track Steve Souders server side *resource.cgi* used by **Cuzillion** for testing browser loading of image, js and css resources under various network conditions:

<http://stevesouders.com/cuzillion/>

There is a generic help page available for using the UI, which can be used to generate URL's for use with *resource.cgi*

<http://stevesouders.com/cuzillion/help.php>

## My fork of Cuzillion

The *metafeather* branch (and others at times) explores providing additional resource types for use in the development and QA of complex web applications and javascript data collection technologies.

### Additional features

1. JSON mime/type and related content type with common error cases such as empty objects, null strings, etc
2. Error and Network status codes such as 401, 403, 404, 500, Browser/proxy Timeouts etc.
3. Plain text option to simulate mis-configured servers serving JSON
4. Generation of javascript to pass cross-domain data via the *window.name* property

Full details can be found in the head of the script, and options can be combined.

More features are added as required during [my](http://uk.linkedin.com/in/liamclancy) job at <http://www.causata.com/>

### Installation

*resource.cgi* is written in Perl and will run as a CGI script under most web servers such as Apache HTTP.

It's suggested that this is used in conjunction with *mod_rewrite* to intercept your applications normal urls to simulate various server-side error conditions, as well as to force the slow loading of asynchronous requests to expose race conditions.

### Examples

Please note that my version of *resource.cgi* defaults to returning JSON data for use in developing AJAX based applications.

    RewriteRule ^/myserver-api/item(.*) http://localhost/tools/cuzillion/resource.cgi?status=401&size=0&path=$1 [P]  # Errors with no content response
    RewriteRule ^/myserver-api/item(.*) http://localhost/tools/cuzillion/resource.cgi?status=403&size=0&path=$1 [P]
    RewriteRule ^/myserver-api/item(.*) http://localhost/tools/cuzillion/resource.cgi?status=404&size=0&path=$1 [P]
    RewriteRule ^/myserver-api/item(.*) http://localhost/tools/cuzillion/resource.cgi?status=500&size=0&path=$1 [P]
    RewriteRule ^/myserver-api/item(.*) http://localhost/tools/cuzillion/resource.cgi?status=503&size=0&path=$1 [P]
    RewriteRule ^/myserver-api/item(.*) http://localhost/tools/cuzillion/resource.cgi?sleep=70&path=$1 [P]           # Force browser connection timeout (Status 0)
    RewriteRule ^/myserver-api/item(.*) http://localhost/tools/cuzillion/resource.cgi?success=false&path=$1 [P]      # Common JS library JSON error property
    RewriteRule ^/myserver-api/item(.*) http://localhost/tools/cuzillion/resource.cgi?size=1&path=$1 [P]             # Empty JSON object
    RewriteRule ^/myserver-api/item(.*) http://localhost/tools/cuzillion/resource.cgi?size=0&path=$1 [P]             # JSON mime/type with no content