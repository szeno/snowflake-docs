description:
:   The SMA-Checkpoints feature supports several configurable settings, which can be modified using either the SMA CLI or the UI application.

# Snowpark Migration Accelerator: Feature Settings

## CLI Commands

A new command has been added to the SMA CLI to disable the SMA-Checkpoints feature. Users can do this by using either of the following flags: `-d` or `--disableCheckpoints`.

### **Like follows:**

Copy code

```
./sma -i inputPath -o outputPath -e user@company.com -c Company -p Project -d
```

Or

Copy code

```
./sma -i inputPath -o outputPath -e user@company.com -c Company -p Project --disableCheckpoints
```

## UI Settings

The SMA application allows users to enable or disable the SMA-Checkpoints feature through the *Conversion Settings* modal, accessible from the conversion settings page.

[![Change conversion Settings](/static/images/migrations/sma-assets/change-conversion-settings.png)](/static/images/migrations/sma-assets/change-conversion-settings.png)

**Configuring SMA-Checkpoints settings**

[![SMA-Checkpoints Settings](/static/images/migrations/sma-assets/image(559).png)](/static/images/migrations/sma-assets/image(559).png)
