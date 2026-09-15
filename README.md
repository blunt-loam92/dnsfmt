# dnsfmt

DNS records copied out of a provider's dashboard, an old zone file, or a
colleague's chat message rarely agree on formatting. TTLs are sometimes
missing, the class field wanders between the second and third column,
`CNAME` shows up lowercase in one line and `A` uppercase in the next, tabs
and spaces are mixed, and trailing dots on names are inconsistent. `dnsfmt`
reads that mess and prints it back out as consistently aligned, uppercased,
fully-qualified records.

It does not resolve, validate rdata against its record type, or talk to any
network — it just cleans up formatting.

## Usage

Given a file `records.txt`:

```
example.com.    3600  IN  A     93.184.216.34
www   in    cname   example.com
mail	MX	10 mail.example.com.
foo.bar.baz.	300	IN	TXT	"v=spf1 include:_spf.google.com ~all"
```

Run:

```
$ python -m dnsfmt.cli records.txt
example.com.      3600  IN  A      93.184.216.34
www.              3600  IN  CNAME  example.com
mail.             3600  IN  MX     10 mail.example.com.
foo.bar.baz.       300  IN  TXT    "v=spf1 include:_spf.google.com ~all"
```

(Once installed with `pip install -e .`, the same works as `dnsfmt records.txt`.)

It also reads from stdin, so it composes with other tools:

```
$ cat records.txt | dnsfmt
$ dig +noall +answer example.com | dnsfmt -
```

Passing no file arguments, or `-` explicitly, both mean "read stdin". Multiple
file arguments are read and formatted together, in order.

Names that don't already end in a dot are qualified with `--origin`:

```
$ echo "www CNAME example.com" | dnsfmt --origin example.com
www.example.com.  3600  IN  CNAME  example.com
```

## Record format

Each input line is read as:

```
NAME [TTL] [CLASS] TYPE RDATA
```

`TTL` and `CLASS` are both optional and may appear in either order — this
matches how real-world input tends to vary. Lines that are blank, or where
everything after a `;` is a comment, are skipped. Anything that can't be
parsed as at least `NAME TYPE RDATA` raises an error naming the offending
line number.

## Status

Early skeleton. Parsing and alignment work for single-line records; there's
no support yet for zone-file features like blank names inheriting the
previous record's name, `$ORIGIN`/`$TTL` directives, or multi-line
parenthesized rdata (e.g. `SOA`).

## License

MIT, see [LICENSE](LICENSE).
