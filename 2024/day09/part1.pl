use strict;
use warnings;
open(my $in, "<", "input.txt") or die "Failed to open input file: $!";

my $line = <$in>;

close $in or die "Failed to close file: $!";

my @blocks = ();

my $id = 0;
for (my $i = 0; $i < length(scalar($line)); $i++) {
    if (substr($line, $i, 1) eq "\n") {
        last;
    }
    my $n = scalar(substr($line, $i, 1));
    for (my $j = 0; $j < $n; $j++) {
        if ($i % 2 == 0) {
            push @blocks, $id;
        } else {
            push @blocks, '.';
        }
    }
    if ($i % 2 == 0) {
        $id++;
    }
}

print("Done parsing file\n");

sub find_first_free_idx() {
    for (my $i = 0; $i < scalar(@blocks); $i++) {
        if ($blocks[$i] eq '.') {
            return $i;
        }
    }
    return -1;
}

sub find_last_num_idx() {
    for (my $i = scalar(@blocks) - 1; $i >= 0; $i--) {
        if ($blocks[$i] ne '.') {
            return $i;
        }
    }
    return -1;
}

sub switch_blocks($$) {
    my ($idx1, $idx2) = @_;
    my $tmp = $blocks[$idx1];
    $blocks[$idx1] = $blocks[$idx2];
    $blocks[$idx2] = $tmp;
}

print "Starting to switch blocks...\n";
while (1) {
    my $first_free_idx = find_first_free_idx();
    my $last_num_idx = find_last_num_idx();

    if ($first_free_idx >= $last_num_idx) {
        last;
    }
    switch_blocks($first_free_idx, $last_num_idx);
}
print "Finished switching blocks\nStarting computing result...\n";

my $result = 0;
for (my $i = 0; $i < scalar(@blocks); $i++) {
    if ($blocks[$i] eq '.') {
        last;
    }
    $result += $i * $blocks[$i];
}

print "$result\n";

