# Guidelines and requirements for listing Apps on Snowflake Marketplace

These guidelines define the enforced standards for publishing applications, both Snowflake Native Apps and Connected Applications, on Snowflake Marketplace.

**On this page:**

1. [Application types on Snowflake Marketplace](#label-guidelines-reqs-application-types)
2. [Native Applications](#native-applications)  
   · [Enforced standards](#label-guidelines-reqs-enforced-standards)
3. [Connected Applications](#label-guidelines-reqs-connected-apps)  
   · [Requirements to publish on Snowflake Marketplace](#label-guidelines-reqs-connected-apps-publish)  
   · [Listing enablement](#label-connected-apps-pre-enablement)

## 1. Application types on Snowflake Marketplace

This page covers listing requirements for two application types on Snowflake Marketplace. Choose the section that matches your product:

**Native Applications**

The Snowflake Native App Framework lets you create data applications that leverage core Snowflake functionality and share data and related business logic through listings on Snowflake Marketplace or private listings. See the [enforced standards](#label-guidelines-reqs-enforced-standards) in the [Native Applications](#native-applications) section below, or see [About the Snowflake Native App Framework](/developer-guide/native-apps/native-apps-about) for an overview.

**Connected Applications**

Connected Applications are external SaaS applications that connect to a consumer’s Snowflake account to read or ingest data. Partners must meet the [requirements to publish](#label-guidelines-reqs-connected-apps-publish) in the [Connected Applications](#label-guidelines-reqs-connected-apps) section below. For background, see [How Connected Applications Work](https://www.snowflake.com/en/blog/powered-by-snowflake-how-connected-applications-work/) and [Connected Applications 101](https://www.snowflake.com/resource/connected-applications-101-what-they-are-and-how-to-build-them/).

If you are listing a Connected Application for the first time, complete the [listing enablement steps](#label-connected-apps-pre-enablement) after you meet the [requirements to publish](#label-guidelines-reqs-connected-apps-publish) in the Connected Applications section below.

## 2. Native Applications

### Publish on Snowflake Marketplace

When your application package is ready to be published on the Snowflake Marketplace, you must submit it to Snowflake for review and approval. The approval process has five phases:

| Phase | Description |
| --- | --- |
| 1. Design and develop | Build your app to meet the [enforced requirements](#label-guidelines-reqs-enforced-standards), keeping core setup, functionality, and authentication on Snowflake. See [About the Native App Framework](/developer-guide/native-apps/native-apps-about). |
| 2. Test your application | [Install and test the app](/developer-guide/native-apps/installing-testing-application) from a separate consumer account, across regions and organizations, to catch installation, privilege, and configuration errors before you submit. |
| 3. Pass the automated security review | Set the application package’s `DISTRIBUTION` to `EXTERNAL` to trigger the [automated security scan](/developer-guide/native-apps/security-overview), then resolve any issues until the version passes. See [Run the security scan](/developer-guide/native-apps/security-run-scan). |
| 4. Submit for functional review | [Create a listing](/collaboration/provider-listings-creating-publishing), attach the security-scanned application package, and submit it to Marketplace Operations for review. |
| 5. Functional review | Marketplace Operations installs and tests your app as a new consumer, then approves it for publishing or returns required changes for you to fix and resubmit. See the [Marketplace trust and safety review process](/collaboration/trust-safety-review-process). |

Expand

Show lessSee more

For step-by-step instructions and FAQs for each phase, see the [Snowflake Marketplace Provider Guide: Native App Approval Process](https://www.snowflake.com/wp-content/uploads/2025/11/Snowflake-Marketplace-Provider-Guide-to-get-a-Native-App-approved-on-the-Marketplace.pdf).

Note

For a diagram of the full approval flow, including how the [automated security scan](/developer-guide/native-apps/security-overview) fits alongside the functional review, see [Snowflake Native App listing approval flow](/collaboration/provider-listings-workflows#label-native-app-listing-approval-flow).

### Standards for Snowflake Native Apps on Snowflake Marketplace

The Snowflake Native App functional review process ensures the quality of apps published on Snowflake Marketplace. To provide clarity into what is evaluated during this process, the following standards apply to all Snowflake Native Apps distributed through Snowflake Marketplace.

**Immediate utility**

The app functionality must be provided within the consumer account and the app must be operational once installed.

**Standalone**

Apps must deliver product experience on Snowflake and facilitate external requirements through Snowflake functionality.

**Data-centric**

Apps should be based on data-centric use cases that leverage data stored in Snowflake.

**Transparent, simple, and secure**

Apps must use Snowflake features to disclose the app’s resource and access requirements and simplify the configuration process for the consumer.

### Enforced standards

Snowflake uses the following requirements to determine if a Snowflake Native App meets the standards for publication on Snowflake Marketplace. These requirements are verified when you submit a listing with an attached application package to Snowflake Marketplace.

1. Immediate utility

   1. Apps must not be shell apps that advertise functionality. Apps must deliver the advertised functionality.
   2. Apps must include a clear framework and instruction for utilizing app functionality.
   3. Apps should not crash, freeze, or otherwise function abnormally.
   4. Apps must list all required credentials and providers must share required credentials with Snowflake at submission for testing.
   5. If apps are not immediately actionable, they must document the expected workflow for a consumer, allowing consumers to fully install and configure the app.
2. Standalone

   1. Apps must not be pass-through. For example, they must not redirect consumers to an external service to enable the app’s core
      functionality.
   2. App interfaces must be accessible after installation directly from Snowflake.
   3. Apps cannot use the Snowflake Marketplace as a distribution platform for cross-selling external applications or services.
   4. Apps that access external services and leverage user authentication should comply with the following standards:
      1. Apps may ask consumers to create a service user in their Snowflake account only to enable access to an external service.

         1. Acceptable authentication methods are Programmatic Access Tokens (PAT), OAuth, or key pair. The service user must be granted only the minimum permissions necessary for the app to function.
      2. Apps that require user authentication should never require the consumer to do the following for authentication:

         1. Input consumer’s Snowflake username and password.
         2. Create a private / public key and share the private key.
3. Data-centric

   1. Apps must leverage Snowflake data in one of the following ways:

      1. Share data from the app provider’s account.
      2. Use datasets from the Snowflake Marketplace.
      3. Access data in the consumer account.
   2. Apps must operate on data that already exists within, or is continuously ingested into, the consumer’s Snowflake environment as part of their existing workflows. Apps that require consumers to create or populate new data objects exclusively for the app to function do not qualify.
4. Transparent and simple

   1. All account-level privileges and references that the app requires must be listed in the application package manifest file.
   2. All resource requirements for the Snowflake Native App must be listed in the [marketplace.yml](/developer-guide/native-apps/marketplace-file) file of the app. The app must create these resources as part of installation and setup.
   3. All account-level privileges and references listed in the application package manifest file must be requested from the consumer through Snowsight or the Python Permission SDK.
   4. Apps must provide a readme file. Apps that do not include a Streamlit or custom user interface must include the following information in the readme file:

      1. A description of what the app does.
      2. The steps the consumer must perform to configure the app after it is installed.
      3. The stored procedures and user-defined functions the app uses.
      4. The privileges the app requires.
      5. Example SQL commands that show consumers how to use the app.
   5. All required SQL commands must be delivered using Snowflake and formatted as code blocks.
   6. If the app provides sample data, you must include procedures on how to use the sample data.
   7. If an application package contains a Streamlit app but does not contain a readme file, you must configure a default [Streamlit app](/developer-guide/native-apps/adding-streamlit#label-streamlit-add-to-manifest).
   8. Apps that use Snowflake Cortex must comply with the following standards:

      1. Apps that call Cortex functions with a specific model (rather than ‘auto’ or a Snowflake-managed model) must document the model name(s) in the listing, application or readme, enabling consumers to evaluate availability in their region. See [Cross-region inference](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cross-region-inference).
      2. Apps must declare SNOWFLAKE.CORTEX\_USER as a required privilege in the application package manifest.yml, rather than requesting broad IMPORTED PRIVILEGES on the SNOWFLAKE database. See [Manifest file privileges](https://docs.snowflake.com/en/developer-guide/native-apps/manifest-reference#privileges-field) and [Calling Cortex functions from an app](https://docs.snowflake.com/en/user-guide/snowflake-cortex/aisql).

### Best practices when publishing a Snowflake Native App

In addition to the requirements for submitting an application package to Snowflake Marketplace, Snowflake also recommends the following best practices when publishing a Snowflake Native App:

- Ensure that all required files are uploaded to the named stage for the version of the app you are submitting, including:

  - The manifest file.
  - The setup script.
  - The README file.
  - Any external stored procedures or user-defined functions required by the application package.
  - Any Streamlit files required by the application package.
  - Any external source code, including Python, Java, etc.
- Ensure that the version of the app you are developing passes the [automated security scan](/developer-guide/native-apps/security-overview).
- Test the new version of your application package by creating the application object locally by using the [CREATE APPLICATION](/sql-reference/sql/create-application) command.

  - Do not add a new version to your application package or set the DISTRIBUTION property to EXTERNAL while you are developing and testing
    an app. These actions trigger the [automated security scan](/developer-guide/native-apps/security-overview). Instead, create the
    application object using [files on a named stage](/developer-guide/native-apps/installing-testing-application#label-native-apps-application-creating-stage).
  - If your app includes a Streamlit app, test the application in Snowsight to ensure the Streamlit app works as expected.
  - Verify that interactions between the Streamlit app and Snowflake Worksheets are seamless and that the consumer does not have to navigate excessively between the two.
- Review all parts of a listing before submitting it for approval.
- Ensure that there are no typos or other textual errors in the listing, readme file, and Streamlit app.

### Recommendations for trial listings

- When an app trial listing expires, Snowflake automatically suspends the app to avoid consumers incurring extra compute costs to the consumer. Snowflake only suspends the objects owned by the app that are currently active. Snowflake does not modify the status of objects that are already suspended.
- When a trial listing is converted to a full or paid listing, Snowflake attempts to re-enable the app by resuming tasks, containers, and compute pools. Snowflake only resumes services and compute pools that have the `auto_resume` property set to false.

### Recommendations for apps with containers

- Compute pools should be set to automatically suspend in combination with Snowpark Container Services jobs to avoid idle compute nodes.
- For higher availability during upgrades and to reduce cold start latency, Snowflake recommends that you set the `MIN_NODES` parameter greater than 1.
- If connections across different services are required in the same app, use the DNS name of the service instead of configuring an external access integration.

### Recommendations for event sharing

- Providers should configure an app to emit log messages and trace events that conform to
  [supported event definitions](/developer-guide/native-apps/ui-consumer-enable-logging#label-nativeapps-consumer-logging-about-event-sharing) to ensure that consumers understand what information is collected.
- Mandatory event definitions should be limited to the log messages and trace events required by the app. Excessive or unnecessary mandatory event definitions should be avoided.
- Adding new mandatory event definitions in a version upgrade must require the consumer re-enable event definitions for the app.
- Use the Python Permission SDK to allow consumers to share optional events.

## 3. Connected Applications

Snowflake allows SaaS providers to list their Connected Applications on Snowflake Marketplace. Connected Applications are integrated SaaS applications that securely connect to a Snowflake customer’s account to read or ingest specified data as part of their workflow. Connected Applications enable consumers to interact with their Snowflake data directly through an external UI.

### Requirements to publish a Connected Application on Snowflake Marketplace

- **Partner network tier:** Providers must be active members of the [Snowflake Partner Network (SPN)](https://www.snowflake.com/en/why-snowflake/partners/), be enrolled in the AI Data Cloud Products Partner Program, and hold a **Connected Application Select** tier designation or higher.
- **CSID requirement:** Each Connected Application must use a Connection String Identifier (CSID) to enable full telemetry and usage tracking. Providers are encouraged to consolidate to a single CSID per application; however, multiple CSIDs are also supported where necessary. The CSID(s) must be initially submitted through SPN and will subsequently be required in your listing submission and verified during the review process.
- **Security transparency:** Providers must complete a short **Security & Data Handling Attestation** as part of the listing process.
- **Listing type:** All Connected Application listings must leverage a public, paid listing and fulfill deals using standard or private offers.

### Ongoing standards for Connected Applications on Snowflake Marketplace

1. **Ecosystem contribution:** Connected Applications should meaningfully contribute to the **Snowflake Data Cloud ecosystem**, helping drive data collaboration, consumption, or workload adoption.
2. **Active partnership:** Providers must be **active contributors** to the Snowflake ecosystem. To remain listed on the Marketplace, providers must maintain their standing within the Partner Network at the **Connected Application Select** tier designation or higher within the AI Data Cloud Products Partner Program, and their application must continue to benefit the ecosystem. Snowflake may remove a listing if the provider is no longer contributing to the ecosystem (per Snowflake’s discretion) or no longer meets partner eligibility standards.

First-time Connected Application providers must meet the [requirements above](#label-guidelines-reqs-connected-apps-publish) for listing eligibility. To verify eligibility and enable your account for listing, complete the [listing enablement steps](#label-connected-apps-pre-enablement) below. Connected Application providers must continually meet the ongoing standards for ecosystem contribution and active partnership.

### Connected Application listing enablement on Snowflake Marketplace

Complete the following steps to verify eligibility against the [requirements to publish a Connected Application on Snowflake Marketplace](#label-guidelines-reqs-connected-apps-publish) and enable your account for listing. Steps 1–3 are submitted through the SPN portal. After submission, Snowflake reviews your inputs and follows up within 10 business days. Reach out to your Partner Development Manager (PDM) for questions, or [submit a case with Marketplace Operations](https://snowforce.my.site.com/s/provider-onboarding-case) for support.

1. **Be an active SPN partner.** Enroll at the **Connected Application Select** tier designation or higher within the AI Data Cloud Products Partner Program.

   - Enroll through the [Snowflake Partner Network (SPN) portal](https://spn.snowflake.com/s/welcome).
   - For tiering requirements, see the [Snowflake Partner Program guide, slide 23](https://docs.google.com/presentation/d/1Mx4M1yUqxsn2Nh-7kAH6Pt-SCwbqWhV4gLY5x-cBHoU/edit?slide=id.g3f137633438_70_1253#slide=id.g3f137633438_70_1253).
2. **Register a valid Connection String Identifier (CSID).** Register a valid CSID for your application.

   - Register your CSID in the [SPN portal](https://spn.snowflake.com/s/welcome).
   - For instructions, see the [Snowflake Partner Program guide, slides 48–49](https://docs.google.com/presentation/d/1Mx4M1yUqxsn2Nh-7kAH6Pt-SCwbqWhV4gLY5x-cBHoU/edit?slide=id.g3129d98d42c_1077_15225#slide=id.g3129d98d42c_1077_15225).
   - For connector best practices, see the [Snowflake Native Connector Best Practices guide](https://drive.google.com/file/d/1brffBv7QXPFzv5lsEtUU9fjD5U8KxcXq/view).
3. **Complete Connected Application technical validation.** Apply for Connected Application technical validation through the SPN portal.

   - For details, see the [Snowflake Partner Program guide, slides 98–101](https://docs.google.com/presentation/d/1Mx4M1yUqxsn2Nh-7kAH6Pt-SCwbqWhV4gLY5x-cBHoU/edit?slide=id.g3ccba5b4430_20_4115#slide=id.g3ccba5b4430_20_4115).
4. **Create a provider profile.** Create a Snowflake Marketplace provider profile if your organization does not already have one.

   - See [Manage your provider profile](/collaboration/provider-profiles-managing) and the [Snowflake Marketplace Provider Playbook, page 46](https://www.snowflake.com/wp-content/uploads/2023/08/sm-provider-playbook-extended-ver.pdf#page=46).
5. **Set up provider payouts (Stripe).** Set up a new Stripe Express connected account for Snowflake Marketplace payouts (no cost). If eligible, you can reuse verified business information from an existing Stripe account instead of completing verification again. To do so, the email address associated with your Snowflake user must match your Stripe sign-in email, and you must be an Administrator or Super Administrator of the existing Stripe account. Your provider billing address must be in an [eligible country](/collaboration/provider-becoming#label-monetization-provider-region-support) to offer paid listings on Snowflake Marketplace.

   - See [Set up Stripe to get paid for listings](/collaboration/provider-becoming#label-set-up-stripe-listings).
   - For Marketplace Capacity Drawdown (MCD) restrictions, see [About committed capacity and Snowflake Marketplace Capacity Drawdown](/collaboration/marketplace-capacity-drawdown).
6. **Wait for Marketplace Operations to enable your account.** After Snowflake validates your SPN submissions and confirms you meet the requirements above, Marketplace Operations enables your account for Connected Application listing. Your Partner Development Manager (PDM) will notify you once your account has been enabled. If you do not have a PDM, Marketplace Operations sends an email to the person who submitted technical validation or to Marketplace profile contacts on file, if available.
7. **Create and publish your listing.** Create and publish your Connected Application listing.

   - See [Create and publish a listing](/collaboration/provider-listings-creating-publishing) and the [Guide to publishing a Connected App](https://www.snowflake.com/wp-content/uploads/2025/11/Guide-to-publishing-a-Connected-App.pdf).
