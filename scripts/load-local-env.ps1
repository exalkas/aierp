# Read the ignored project .env without expanding dollar signs in secret values.
$environmentFile = Join-Path (Split-Path $PSScriptRoot -Parent) ".env"
if (Test-Path -LiteralPath $environmentFile) {
    foreach ($line in Get-Content -LiteralPath $environmentFile) {
        if ($line.TrimStart().StartsWith("#") -or $line -notmatch '^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=(.*)$') {
            continue
        }
        $variableName = $Matches[1]
        $variableValue = $Matches[2].Trim()
        if ($variableValue.Length -ge 2 -and (
            ($variableValue.StartsWith('"') -and $variableValue.EndsWith('"')) -or
            ($variableValue.StartsWith("'") -and $variableValue.EndsWith("'"))
        )) {
            $variableValue = $variableValue.Substring(1, $variableValue.Length - 2)
        }
        if ($null -eq [Environment]::GetEnvironmentVariable($variableName, "Process")) {
            [Environment]::SetEnvironmentVariable($variableName, $variableValue, "Process")
        }
    }
}
