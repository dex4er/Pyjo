#!/usr/bin/env perl

use v5.14;

use Mojo::IOLoop;

sub step1 {
    my ($delay) = @_;
    say "Step 1";
    Mojo::IOLoop->timer(2 => $delay->begin);
    Mojo::IOLoop->timer(1 => $delay->begin);
    say 'Wait 2 seconds for step 2.';
}

sub step2 {
    say "Step 2";
    my ($delay) = @_;
    Mojo::IOLoop->delay->steps(sub {
        my ($delay2) = @_;
        say "Step 2.1";
        my $end = $delay2->begin;
        Mojo::IOLoop->timer(1 => sub { $end->('','OK') });
        say 'Wait 1 second for step 2.2.';
    }, sub {
        my ($delay2, @args) = @_;
        say "Step 2.2 got @args";
        Mojo::IOLoop->timer(3 => $delay2->begin);
        say 'Wait 3 seconds for step 3.';
    }, $delay->begin);
}

sub step3 {
    my ($delay) = @_;
    say "Step 3";
    say 'And done.';
}

Mojo::IOLoop->delay->steps(
    \&step1,
    \&step2,
    \&step3,
)->wait;

say "END";
