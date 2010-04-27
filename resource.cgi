#!/usr/local/bin/perl

# $Header: /home/sowrock/cvsroot/stevesouders.com/examples/sleep.txt,v 1.2 2007/09/02 07:52:39 sowrock Exp $

################################################################################
# This CGI is used to simulate different types of components in an HTML page
# that take different lengths of time. Here are the CGI params and legal values:
#     type=[gif|js|css|html|swf]
#           default is "gif"
#     sleep=N
#           N is a number of seconds for the server to wait before returning the response
#           default is 0
#     expires=[-1|0|1]
#          -1   return an Expires header in the past
#           0   do not return an Expires header
#           1   return an Expires header in the future (default)
#     last=[-1|0]
#          -1   return a Last-Modified header equal to the file's timestamp (default)
#           0   do not return a Last-Modified header
#     redir=1
#           1 means return a 302 redirect response that redirects right back with the "redir=1" removed
################################################################################

my $gQuerystring;
my %gParams;

main();

exit 0;


sub main {
    parseParams();

    sleep($gParams{'sleep'}) if ( 0 < $gParams{'sleep'} );

    print genHeaders();

    print genContent();
}


sub parseParams {
    my $querystring = "";

    if ($ENV{'REQUEST_METHOD'} eq 'GET') {
        $querystring = $ENV{'QUERY_STRING'};
    }
    elsif ($ENV{'REQUEST_METHOD'} eq 'POST') {
        read(STDIN, $querystring, $ENV{'CONTENT_LENGTH'});
    }
    $gQuerystring = $querystring;

    # Defaults:
    $gParams{'type'} = "gif";
    $gParams{'sleep'} = 0;
    $gParams{'expires'} = 1;  # future Expires header
    $gParams{'last'} = -1;   # Last-Modified equal to file timestamp

    # Now parse the CGI querystring.
    if ( $querystring && "" ne $querystring ) {
        foreach my $tuple ( split(/&/, $querystring) ) {
            my ($key, $value) = split(/=/, $tuple);
            $gParams{$key} = $value;
        }
    }
}


sub genHeaders {
    my $headers = "";
    my $type = $gParams{'type'};

    if ( $gParams{'redir'} ) {
        my $querystring = $gQuerystring;

	# Remove the redir param from the querystring.
        $querystring =~ s/[&]*redir=[^&]*//g;
        $querystring =~ s/^&//;  # make sure it doesn't start with "&"

        my $uri = $ENV{'REQUEST_URI'};
        $uri = $1 if ( $uri =~ /^(.*)\?/ );
        my $host = $ENV{'HTTP_HOST'};
        my $port = $ENV{'SERVER_PORT'};
        my $location = ( 443 == $port ? "https://" : "http://" ) . "$host$uri?$querystring";
        $headers = "Content-Type: text/css\nLocation: $location\n";
    }
    elsif ( "css" eq $type ) {
        $headers = "Content-Type: text/css\n";
    }
    elsif ( "js" eq $type ) {
        $headers = "Content-Type: application/x-javascript\n";
    }
    elsif ( "html" eq $type ) {
        $headers = "Content-Type: text/html\n";
    }
    elsif ( "swf" eq $type ) {
        $headers = "Content-Type: application/x-shockwave-flash\n";
    }
    else {  # gif
        $headers = "Content-Type: image/gif\n";
    }

    # If requested, include a Last-Modified header in the past and a far future Expires header.
    if ( $gParams{'expires'} ) {
	my $epoch = ( -1 == $gParams{'expires'} ? time() - 30*24*60*60 : time() + 30*24*60*60 );
	my ($sec, $min, $hour, $day, $month, $year, $wday) = gmtime($epoch);
	$year += 1900;
	my $expires =  sprintf("Expires: %s, %.2d %s %d %.2d:%.2d:%.2d GMT\n",
			       ("Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat")[$wday],
			       $day, 
			       ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")[$month],
			       $year, $hour, $min, $sec);
	$headers .= $expires;
    }

    # If requested, include a Last-Modified header in the past and a far future Expires header.
    if ( -1 == $gParams{'last'} ) {
	# We don't really have a timestamp for a file on disk (since we generate the content on-the-fly),
	# so let's just pick a fixed time in the past since most items would have a timestamp in the past.
	# noon 1/15/2006 GMT = 1137326400
	my $epoch = 1137326400;
	my ($sec, $min, $hour, $day, $month, $year, $wday) = gmtime($epoch);
	$year += 1900;
	my $last =  sprintf("Last-Modified: %s, %.2d %s %d %.2d:%.2d:%.2d GMT\n",
			    ("Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat")[$wday],
			    $day, 
			    ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")[$month],
			    $year, $hour, $min, $sec);
	$headers .= $last;
    }

    return $headers . "\n";  # need two returns at the end of the headers
}


sub genContent {
    my $type = $gParams{'type'};
    my $content = "";

    if ( "css" eq $type ) {
        $content = ".sleepcgi { background: #EEE; color: #606; font-weight: bold; padding: 10px; }\n";
    }
    elsif ( "js" eq $type ) {
        $content = "var sleepcgi = 1;\nfunction sleepcgiFunc() {\n    sleepcgi++;\n}\n";
    }
    elsif ( "html" eq $type ) {
        $content = <<OUTPUT
<html>
<head>
<title>sleep.cgi test page</title>
</head>
<body>
sleep.cgi test page
</body>
</html>
OUTPUT
    ;
    }
    elsif ( "swf" eq $type ) {
        # Just echo a file from disk. Copy a Flash file to this directory and name it "sleep.swf".
        my $file = "./sleep.swf";
        if ( -e $file ) {
	    open(IN, $file);
	    while(<IN>) {
		my $line = $_;
		$content .= $line;
	    }
	}
    }
    else {  # "gif"
        # Just echo a file from disk. Copy a GIF image file to this directory and name it "sleep.gif".
        my $file = "./sleep.gif";
        if ( -e $file ) {
	    open(IN, $file);
	    while(<IN>) {
		my $line = $_;
		$content .= $line;
	    }
	}
    }

    return $content;
}



