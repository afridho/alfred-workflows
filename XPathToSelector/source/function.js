function run(argv) {
  var Path = argv[0].trim();

  Path = Path.replace(/^\/+/,"");
  Path = Path.replace(/\[([0-9])+\]/g,":nth-of-type($1)");
  Path = Path.replace(/\//g,"\x20>");
  return (Path)
}