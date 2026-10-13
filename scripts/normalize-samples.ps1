param(
    [switch]$Write
)

$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent $PSScriptRoot
$samplesRoot = Join-Path $repoRoot 'samples'
$fallbackMarkdownPath = '../../../images/ilovecopilot.png'
$fallbackImageUrl = 'https://github.com/pnp/copilot-prompts/raw/main/images/ilovecopilot.png'
$trackerBaseUrl = 'https://m365-visitor-stats.azurewebsites.net/copilot-prompts/'
$issues = [System.Collections.Generic.List[string]]::new()
$changes = [System.Collections.Generic.List[string]]::new()

function Set-FileText {
    param([string]$Path, [string]$Content)

    if ($Write) {
        [System.IO.File]::WriteAllText($Path, $Content, [System.Text.UTF8Encoding]::new($false))
    }
}

function Add-Issue {
    param([string]$Message)

    $issues.Add($Message)
}

function Add-Change {
    param([string]$Message)

    $changes.Add($Message)
}

function Get-SampleDirectories {
    $categories = Get-ChildItem $samplesRoot -Directory | Where-Object Name -in @('prompts', 'agent-instructions', 'skills')
    foreach ($category in $categories) {
        Get-ChildItem $category.FullName -Directory | ForEach-Object {
            [pscustomobject]@{
                Category = $category.Name
                Directory = $_
            }
        }
    }
}

function Get-Taxonomy {
    param([string]$Category)

    switch ($Category) {
        'prompts' { 'prompt' }
        'agent-instructions' { 'agent' }
        'skills' { 'skill' }
        default { throw "Unknown sample category: $Category" }
    }
}

function Get-FirstHeading {
    param([string]$ReadmePath, [string]$Fallback)

    $heading = Get-Content $ReadmePath | Where-Object { $_ -match '^#\s+(.+)$' } | Select-Object -First 1
    if ($heading) {
        return ($heading -replace '^#\s+', '').Trim()
    }

    return $Fallback
}

function New-Metadata {
    param(
        [string]$Category,
        [string]$Slug,
        [string]$ReadmePath
    )

    $title = Get-FirstHeading -ReadmePath $ReadmePath -Fallback $Slug
    $description = "A contributed Copilot sample for $title."
    $product = if ($Category -eq 'skills') { 'GitHub Copilot' } elseif ($Category -eq 'agent-instructions') { 'Copilot' } else { 'Microsoft 365 Copilot' }
    $author = if ($Slug -eq 'm365-change-impacts') {
        [ordered]@{ gitHubAccount = 'dzblanco08'; pictureUrl = 'https://github.com/dzblanco08.png'; name = 'Delia Zuniga' }
    } elseif ($Slug -eq 'm365-copilot-as-a-professional-executive-assistant') {
        [ordered]@{ gitHubAccount = 'ojopiyo'; pictureUrl = 'https://github.com/ojopiyo.png'; name = 'Josiah Opiyo' }
    } else {
        [ordered]@{ gitHubAccount = 'pnp'; pictureUrl = 'https://github.com/pnp.png'; name = 'PnP Community' }
    }
    $date = if ($Slug -eq 'm365-change-impacts') { '2026-02-28' } elseif ($Slug -eq 'm365-copilot-as-a-professional-executive-assistant') { '2026-02-02' } else { '2026-09-03' }

    return [ordered]@{
        name = ''
        source = 'pnp'
        title = $title
        shortDescription = $description
        url = ''
        downloadUrl = ''
        longDescription = @($description)
        creationDateTime = $date
        updateDateTime = $date
        products = @($product)
        metadata = @()
        thumbnails = @()
        authors = @($author)
        references = @()
    }
}

function Set-Property {
    param(
        [object]$Object,
        [string]$Name,
        [object]$Value
    )

    if ($Object.PSObject.Properties.Name -contains $Name) {
        $Object.$Name = $Value
    } else {
        $Object | Add-Member -NotePropertyName $Name -NotePropertyValue $Value
    }
}

function Test-ReadmeHasContentImage {
    param([string]$Content)

    $withoutTrackers = $Content -replace '(?im)^.*https://m365-visitor-stats\.azurewebsites\.net/(?:SamplesGallery|copilot-prompts)/.*(?:\r?\n)?', ''
    return $withoutTrackers -match '!\[[^\]]*\]\([^)]+\)|<img\s+[^>]*src\s*=|<picture\b'
}

function Get-ImageFiles {
    param([System.IO.DirectoryInfo]$SampleDirectory)

    return @(Get-ChildItem $SampleDirectory.FullName -Recurse -File | Where-Object Extension -match '^\.(png|jpe?g|gif|webp)$')
}

function Get-PreferredImageFile {
    param([System.IO.FileInfo[]]$Images)

    return $Images | Sort-Object `
        @{ Expression = { if ($_.BaseName -match '^(preview|demo|sample|screenshot)') { 0 } else { 1 } } }, `
        @{ Expression = {
            switch ($_.Extension.ToLowerInvariant()) {
                '.png' { 0 }
                '.jpg' { 1 }
                '.jpeg' { 1 }
                '.webp' { 2 }
                '.gif' { 3 }
                default { 4 }
            }
        } }, `
        FullName | Select-Object -First 1
}

function Get-RawImageUrl {
    param(
        [string]$Category,
        [string]$Slug,
        [System.IO.FileInfo]$Image
    )

    $samplePath = Join-Path (Join-Path $samplesRoot $Category) $Slug
    $relativePath = [System.IO.Path]::GetRelativePath($samplePath, $Image.FullName).Replace('\', '/')
    $encodedPath = ($relativePath.Split('/') | ForEach-Object { [uri]::EscapeDataString($_) }) -join '/'
    return "https://github.com/pnp/copilot-prompts/raw/main/samples/$Category/$Slug/$encodedPath"
}

function Get-MarkdownImagePath {
    param(
        [System.IO.DirectoryInfo]$SampleDirectory,
        [System.IO.FileInfo]$Image
    )

    $relativePath = [System.IO.Path]::GetRelativePath($SampleDirectory.FullName, $Image.FullName).Replace('\', '/')
    $encodedPath = ($relativePath.Split('/') | ForEach-Object { [uri]::EscapeDataString($_) }) -join '/'
    return "./$encodedPath"
}

$sampleDirectories = @(Get-SampleDirectories)

foreach ($sample in $sampleDirectories) {
    $category = $sample.Category
    $directory = $sample.Directory
    $slug = $directory.Name
    $taxonomy = Get-Taxonomy $category
    $identity = "copilotprompts-$taxonomy-$slug"
    $relativeSamplePath = "samples/$category/$slug"

    $readme = Get-ChildItem $directory.FullName -File | Where-Object { $_.Name -ieq 'README.md' } | Select-Object -First 1
    if (-not $readme) {
        Add-Issue "${relativeSamplePath}: README.md is missing"
        continue
    }

    if ($readme.Name -cne 'README.md') {
        Add-Change "${relativeSamplePath}: rename $($readme.Name) to README.md"
        if ($Write) {
            $temporaryReadme = Join-Path $directory.FullName '__README.tmp'
            Move-Item $readme.FullName $temporaryReadme
            Move-Item $temporaryReadme (Join-Path $directory.FullName 'README.md')
            $readme = Get-Item (Join-Path $directory.FullName 'README.md')
        }
    }

    $assetsDirectory = Get-ChildItem $directory.FullName -Directory | Where-Object { $_.Name -ieq 'assets' } | Select-Object -First 1
    if ($assetsDirectory -and $assetsDirectory.Name -cne 'assets') {
        Add-Change "${relativeSamplePath}: rename $($assetsDirectory.Name) to assets"
        if ($Write) {
            $temporaryAssets = Join-Path $directory.FullName '__assets.tmp'
            Move-Item $assetsDirectory.FullName $temporaryAssets
            Move-Item $temporaryAssets (Join-Path $directory.FullName 'assets')
            $assetsDirectory = Get-Item (Join-Path $directory.FullName 'assets')
        }
    }

    if (-not $assetsDirectory) {
        Add-Change "${relativeSamplePath}: create assets directory"
        if ($Write) {
            $assetsDirectory = New-Item (Join-Path $directory.FullName 'assets') -ItemType Directory
        }
    }

    $canonicalMetadataPath = Join-Path $directory.FullName 'assets/sample.json'
    $metadataFile = if (Test-Path $canonicalMetadataPath) {
        Get-Item $canonicalMetadataPath
    } else {
        Get-ChildItem $directory.FullName -Recurse -File -Filter 'sample.json' | Select-Object -First 1
    }

    if ($metadataFile -and $metadataFile.FullName -ne $canonicalMetadataPath) {
        Add-Change "${relativeSamplePath}: move sample.json to assets/sample.json"
        if ($Write) {
            Move-Item $metadataFile.FullName $canonicalMetadataPath
            $metadataFile = Get-Item $canonicalMetadataPath
        }
    }

    if (-not $metadataFile) {
        Add-Change "${relativeSamplePath}: create assets/sample.json"
        $metadata = New-Metadata -Category $category -Slug $slug -ReadmePath $readme.FullName
    } else {
        try {
            $parsedMetadata = Get-Content $metadataFile.FullName -Raw | ConvertFrom-Json -NoEnumerate
        } catch {
            Add-Issue "${relativeSamplePath}: sample.json is invalid JSON: $($_.Exception.Message)"
            continue
        }

        if ($parsedMetadata -is [System.Array]) {
            if ($parsedMetadata.Count -ne 1) {
                Add-Issue "${relativeSamplePath}: sample.json must contain exactly one item"
                continue
            }
            $metadata = $parsedMetadata[0]
        } else {
            Add-Change "${relativeSamplePath}: wrap sample.json object in an array"
            $metadata = $parsedMetadata
        }
    }

    $expectedUrl = "https://github.com/pnp/copilot-prompts/tree/main/$relativeSamplePath"
    $expectedDownloadUrl = "https://pnp.github.io/download-partial/?url=$expectedUrl"
    Set-Property $metadata 'name' $identity
    Set-Property $metadata 'source' 'pnp'
    Set-Property $metadata 'url' $expectedUrl
    Set-Property $metadata 'downloadUrl' $expectedDownloadUrl

    foreach ($arrayProperty in @('longDescription', 'products', 'metadata', 'thumbnails', 'authors', 'references')) {
        if (-not ($metadata.PSObject.Properties.Name -contains $arrayProperty) -or $null -eq $metadata.$arrayProperty) {
            Set-Property $metadata $arrayProperty @()
        }
    }

    if (-not $metadata.title) {
        Set-Property $metadata 'title' (Get-FirstHeading -ReadmePath $readme.FullName -Fallback $slug)
    }
    if (-not $metadata.shortDescription) {
        Set-Property $metadata 'shortDescription' "A contributed Copilot sample for $($metadata.title)."
    }
    if (@($metadata.longDescription).Count -eq 0) {
        Set-Property $metadata 'longDescription' @($metadata.shortDescription)
    }
    if (@($metadata.products).Count -eq 0) {
        $defaultProduct = if ($category -eq 'skills') { 'GitHub Copilot' } elseif ($category -eq 'agent-instructions') { 'Copilot' } else { 'Microsoft 365 Copilot' }
        Set-Property $metadata 'products' @($defaultProduct)
    }
    if (-not $metadata.creationDateTime) {
        Set-Property $metadata 'creationDateTime' '2026-09-03'
    }
    if (-not $metadata.updateDateTime -or ([datetime]$metadata.updateDateTime -lt [datetime]$metadata.creationDateTime)) {
        Set-Property $metadata 'updateDateTime' $metadata.creationDateTime
    }

    $imageFiles = Get-ImageFiles $directory
    $preferredImage = Get-PreferredImageFile $imageFiles
    $previewUrl = if (-not $preferredImage) {
        $fallbackImageUrl
    } else {
        Get-RawImageUrl -Category $category -Slug $slug -Image $preferredImage
    }
    $imageThumbnails = @($metadata.thumbnails | Where-Object { $_.type -eq 'image' } | Sort-Object order)
    if ($imageThumbnails.Count -eq 0) {
        Add-Change "${relativeSamplePath}: add gallery preview thumbnail"
        Set-Property $metadata 'thumbnails' @([ordered]@{
            type = 'image'
            order = 100
            url = $previewUrl
            alt = "$($metadata.title) preview"
        })
    } else {
        $primaryThumbnail = $imageThumbnails[0]
        if ($primaryThumbnail.url -ne $previewUrl) {
            $previewKind = if ($preferredImage) { 'sample-specific' } else { 'shared fallback' }
            Add-Change "${relativeSamplePath}: use $previewKind thumbnail"
            Set-Property $primaryThumbnail 'url' $previewUrl
        }
        if ([string]::IsNullOrWhiteSpace($primaryThumbnail.alt)) {
            Add-Change "${relativeSamplePath}: add thumbnail alt text"
            Set-Property $primaryThumbnail 'alt' "$($metadata.title) preview"
        }
    }

    $thumbnailOrders = @{}
    foreach ($thumbnail in $imageThumbnails) {
        if ([string]::IsNullOrWhiteSpace([string]$thumbnail.url) -or [string]::IsNullOrWhiteSpace([string]$thumbnail.alt)) {
            Add-Issue "${relativeSamplePath}: every image thumbnail requires a URL and alt text"
        }

        $thumbnailOrder = [string]$thumbnail.order
        if ($thumbnailOrders.ContainsKey($thumbnailOrder)) {
            Add-Issue "${relativeSamplePath}: image thumbnail order $thumbnailOrder is duplicated"
        } else {
            $thumbnailOrders[$thumbnailOrder] = $true
        }
    }

    foreach ($author in @($metadata.authors)) {
        if ([string]::IsNullOrWhiteSpace([string]$author.gitHubAccount) -or [string]::IsNullOrWhiteSpace([string]$author.name)) {
            Add-Issue "${relativeSamplePath}: every author requires gitHubAccount and name"
        }
    }

    $metadataJson = (ConvertTo-Json -InputObject @($metadata) -Depth 20).Replace("`r`n", "`n")
    $existingMetadataJson = if (Test-Path $canonicalMetadataPath) { (Get-Content $canonicalMetadataPath -Raw).Trim() } else { '' }
    if ($existingMetadataJson -ne $metadataJson.Trim()) {
        Add-Change "${relativeSamplePath}: normalize sample.json"
        Set-FileText -Path $canonicalMetadataPath -Content ($metadataJson + "`n")
    }

    $existingReadmeContent = [System.IO.File]::ReadAllText($readme.FullName)
    $readmeContent = $existingReadmeContent.Replace("`r`n", "`n").Replace("`r", "`n")
    $newline = "`n"
    $withoutTrackers = [regex]::Replace(
        $readmeContent,
        '(?im)^.*https://m365-visitor-stats\.azurewebsites\.net/(?:SamplesGallery|copilot-prompts)/.*(?:\r?\n)?',
        ''
    ).TrimEnd()
    $withoutTrackers = [regex]::Replace($withoutTrackers, '\r?\n---[ \t]*$', '').TrimEnd()

    if ($preferredImage -and $withoutTrackers.Contains("![Default sample preview]($fallbackMarkdownPath)")) {
        $contributedImagePath = Get-MarkdownImagePath -SampleDirectory $directory -Image $preferredImage
        Add-Change "${relativeSamplePath}: use contributed README preview image"
        $withoutTrackers = $withoutTrackers.Replace(
            "![Default sample preview]($fallbackMarkdownPath)",
            "![Sample preview]($contributedImagePath)"
        )
    }

    if (-not (Test-ReadmeHasContentImage $readmeContent)) {
        Add-Change "${relativeSamplePath}: add README preview image"
        $readmePreview = if (-not $preferredImage) {
            "![Default sample preview]($fallbackMarkdownPath)"
        } else {
            $contributedImagePath = Get-MarkdownImagePath -SampleDirectory $directory -Image $preferredImage
            "![Sample preview]($contributedImagePath)"
        }
        $withoutTrackers += "$newline$newline$readmePreview"
    }

    $expectedTracker = "![]($trackerBaseUrl$identity)"
    $normalizedReadme = "$withoutTrackers$newline$newline---$newline$expectedTracker$newline"
    if ($existingReadmeContent -ne $normalizedReadme) {
        Add-Change "${relativeSamplePath}: normalize final visitor tracker"
        Set-FileText -Path $readme.FullName -Content $normalizedReadme
    }
}

if ($issues.Count -gt 0) {
    $issues | ForEach-Object { Write-Error $_ }
    exit 1
}

if ($changes.Count -gt 0) {
    $changes | Sort-Object -Unique | ForEach-Object { Write-Output $_ }
    if (-not $Write) {
        Write-Error "$($changes.Count) normalization changes are required. Run this script with -Write."
        exit 1
    }
}

Write-Output "Validated $($sampleDirectories.Count) sample folders."