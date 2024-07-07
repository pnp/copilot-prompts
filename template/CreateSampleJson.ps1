# Define the path to the JSON file and the placeholders file
$jsonFilePath = 'sample-template-2.json'
$jsonOutputFilePath = 'sample.json'
$dataFilePath = 'placeholders.txt'

# Load the JSON file
$jsonContent = (Get-Content $jsonFilePath -Raw )

# Read the data file
$data = Get-Content $dataFilePath

# Loop over each line in the data file
foreach ($line in $data) {
    # Split the line into a key and a value
    $parts = $line -split '='
    $name = $parts[0]
    $value = $parts[1]

    Write-Host "Replacing $name with $value"
    $jsonContent = $jsonContent -replace "YOUR-$($name.ToUpper())", $value
}

# Write the updated string back to the file
$jsonContent | Set-Content $jsonOutputFilePath
