use strict;
use warnings;
open(my $in, "<", "input.txt") or die "Failed to open input file: $!";

my $line = <$in>;

close $in or die "Failed to close file: $!";

my @files = ();
my @free_spaces = ();

my $total_length = 0;
my $start = 0;
my $id = 0;
for (my $i = 0; $i < length(scalar($line)); $i++) {
    if (substr($line, $i, 1) eq "\n") {
        last;
    }
    my $length = scalar(substr($line, $i, 1));
    if ($i % 2 == 0) {
        my $file = bless {
            id => $id,
            length => $length,
            start => $start
        };
        push @files, $file;
        $id++;
    } else {
        if ($length > 0) {
            my $free_space = bless {
                start => $start,
                length => $length
            };
            push @free_spaces, $free_space;
        }
    }
    $start += $length;
    $total_length += $length;
}

sub find_free_space_index_of_size($) {
    my ($size) = @_;
    for (my $i = 0; $i < scalar(@free_spaces); $i++) {
        if ($free_spaces[$i]->{length} >= $size) {
            return $i;
        }
    }
    return -1;
}

sub find_free_space_index_before_start($) {
    my ($file_start) = @_;
    for (my $i = 0; $i < scalar(@free_spaces); $i++) {
        if ($free_spaces[$i]->{start} + $free_spaces[$i]->{length} + 1 == $file_start) {
            return $i;
        }
    }
    return -1;
}

@files = sort { $b->{id} <=> $a->{id} } @files;
for (my $i = 0; $i < scalar(@files); $i++) {
    my $file = $files[$i];
    my $free_space_idx = find_free_space_index_of_size($file->{length});

    if ($free_space_idx != -1 && $free_spaces[$free_space_idx]->{start} < $file->{start}) {
        $file->{start} = $free_spaces[$free_space_idx]->{start};
        $free_spaces[$free_space_idx]->{length} -= $file->{length};
        $free_spaces[$free_space_idx]->{start} += $file->{length};

        if ($free_spaces[$free_space_idx]->{length} == 0) {
            splice @free_spaces, $free_space_idx, 1;
        }
    }
}
@files = sort { $a->{start} <=> $b->{start} } @files;

my $result = 0;
for (my $i = 0; $i < scalar(@files); $i++) {
    my $file = $files[$i];
    for (my $j = $file->{start}; $j < $file->{start} + $file->{length}; $j++) {
        $result += $j * $file->{id};
    }
}

print "$result\n";
