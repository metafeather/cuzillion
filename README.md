# Overview

This repository attempts to track Steve Souders server side *resource.cgi* used by **Cuzillion** for testing browser loading of image, js and css resources under various network conditions:

<http://stevesouders.com/cuzillion/>

There is a generic help page available for using the UI, which can be used to generate URL's for use with *resource.cgi*

<http://stevesouders.com/cuzillion/help.php>

## My fork of Cuzillion

The *metafeather* branch (and others at times) explores providing additional resource types for use in the development and QA of complex web applications and javascript data collection technologies.

### Additional features

1. Error and Network status codes such as 401, 403, 404, 500, Browser/proxy Timeouts etc.
2. JSON mime/type and related content type with common error cases such as empty objects, null strings, etc
3. Plain text option to simulate mis-configured servers serving JSON
4. Generation of javascript to pass cross-domain data via the *window.name* property

Full details can be found in the head of the script, and options can be combined.

More features are added as required during [my](http://uk.linkedin.com/in/liamclancy) job at <http://www.causata.com/>

### Installation

*resource.cgi* is written in Perl and will run as a CGI script under most web servers such as Apache HTTP.