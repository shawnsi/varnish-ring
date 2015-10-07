backend default {
  .host = "127.0.0.1";
  .port = "9090";
}

sub vcl_deliver {
  if (obj.hits > 0) {
    set resp.http.X-Cache = "HIT";
  }
  else {
    set resp.http.X-Cache = "MISS";
  }
}
