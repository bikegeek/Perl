#!/usr/bin/perl
'''A little test program to see how to throw/raise an exception in perl
'''


use Try::Tiny;
try{
    for ($i=0;$i<11;$i++){
        &tryit($i);
        print "....A-OK!\n";
    }
} catch{
    warn "caught error $_";
};


print "Second loop, to mimic what we need in parsePirep main code...\n";
for ($i=0;$i<11;$i++){
    try{
        &tryit($i)
    } catch{
        print "error found $_\n";
        last;
    };
}

sub tryit($i){
    if ($i == 5){
#        die "Exceptional case i = 5";
         # Test if we get a divide by zero error when we catch
         2/0;
    }else{
        print "input value for i = $i\n";
    }
 }


