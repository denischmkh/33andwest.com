import requests

from load_django import *
from parser_app.models import Artist

from django.utils import timezone
today = timezone.now().date()

# url = "https://siteassets.parastorage.com/pages/pages/thunderbolt"
url = 'https://siteassets.parastorage.com/pages/pages/thunderbolt?appDefinitionIdToSiteRevision=%7B%2214271d6f-ba62-d045-549b-ab972ae1f70e%22%3A%2225%22%2C%2214bcded7-0066-7c35-14d7-466cb3f09103%22%3A%221335%22%7D&beckyExperiments=.DatePickerPortal%2C.EnableCustomCSSVarsForLoginSocialBar%2C.LoginBarEnableLoggingInStateInSSR%2C.TextInputAutoFillFix%2C.UseLoginSocialBarCustomMenu%2C.WixFreeSiteBannerDesktop%2C.WixFreeSiteBannerMobile%2C.buttonUdp%2C.calculateCollapsibleTextLineHeightByFont%2C.classicPaginationAsList%2C.cssInBlocks%2C.dropAppsClientSpecMapByApplicationId%2C.dynamicSlots%2C.fiveGridLineStudioSkins%2C.imageEncodingAVIF%2C.includeGhostsInTpaPageConfig%2C.inlineFontsCSSForIframeTPA%2C.isClassNameToRootEnabled%2C.propsCarmiMappersMigration1%2C.propsCarmiMappersMigration2%2C.propsCarmiMappersMigration4%2C.propsCarmiMappersMigration5%2C.removeFrozenFooterFromAnchors%2C.runSvgLoaderFeatureOnBreadcrumbsComp%2C.shouldUseResponsiveImages%2C.soapOffsetRefactor%2C.svgResolver_2%2C.updateRichTextSemanticClassNamesOnCorvid%2C.useImageAvifFormatInNativeProGallery%2C.useResponsiveImgClassicFixed&blocksBuilderManifestGeneratorVersion=1.129.0&contentType=application%2Fjson&deviceType=Desktop&dfCk=6&dfVersion=1.4886.0&disableStaticPagesUrlHierarchy=false&editorName=Unknown&experiments=dm_bgScrubToMotionFixer%2Cdm_deleteLayoutOverridesForRefComponents%2Cdm_migrateOldHoverBoxToNewFixer&externalBaseUrl=https%3A%2F%2Fwww.prensadanna.com.mx&fileId=6310029d.bundle.min&formFactor=desktop&hasTPAWorkerOnSite=false&isClientSdkOnSite=true&isHttps=true&isInSeo=false&isMultilingualEnabled=false&isPremiumDomain=true&isTrackClicksAnalyticsEnabled=false&isUrlMigrated=true&isWixCodeOnPage=false&isWixCodeOnSite=false&language=en&languageResolutionMethod=QueryParam&metaSiteId=5d514a92-27db-44df-83d2-57584b594a38&migratingToOoiWidgetIds=14fd5970-8072-c276-1246-058b79e70c1a&module=thunderbolt-features&oneDocEnabled=true&originalLanguage=en&pageId=a5fc37_5be91821e604070e846e614f3c524973_1709.json&quickActionsMenuEnabled=false&registryLibrariesTopology=%5B%7B%22artifactId%22%3A%22editor-elements%22%2C%22namespace%22%3A%22wixui%22%2C%22url%22%3A%22https%3A%2F%2Fstatic.parastorage.com%2Fservices%2Feditor-elements%2F1.14104.0%22%7D%2C%7B%22artifactId%22%3A%22editor-elements%22%2C%22namespace%22%3A%22dsgnsys%22%2C%22url%22%3A%22https%3A%2F%2Fstatic.parastorage.com%2Fservices%2Feditor-elements%2F1.14104.0%22%7D%5D&remoteWidgetStructureBuilderVersion=1.251.0&siteId=d5bd1aa5-083a-4a15-bcd4-a8ad2280a0c3&siteRevision=1711&staticHTMLComponentUrl=https%3A%2F%2Fwww-prensadanna-com-mx.filesusr.com%2F&useSandboxInHTMLComp=false&viewMode=desktop'
website_link = 'https://www.prensadanna.com.mx'

headers = {
    "Referer": "https://www.prensadanna.com.mx/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
}

params = {
    "appDefinitionIdToSiteRevision": '{"14271d6f-ba62-d045-549b-ab972ae1f70e":"25","14bcded7-0066-7c35-14d7-466cb3f09103":"1335"}',
    "beckyExperiments": ".DatePickerPortal,.EnableCustomCSSVarsForLoginSocialBar,.LoginBarEnableLoggingInStateInSSR,.TextInputAutoFillFix,.UseLoginSocialBarCustomMenu,.WixFreeSiteBannerDesktop,.WixFreeSiteBannerMobile,.buttonUdp,.calculateCollapsibleTextLineHeightByFont,.classicPaginationAsList,.cssInBlocks,.dropAppsClientSpecMapByApplicationId,.dynamicSlots,.fiveGridLineStudioSkins,.imageEncodingAVIF,.includeGhostsInTpaPageConfig,.inlineFontsCSSForIframeTPA,.isClassNameToRootEnabled,.propsCarmiMappersMigration1,.propsCarmiMappersMigration2,.propsCarmiMappersMigration4,.propsCarmiMappersMigration5,.removeFrozenFooterFromAnchors,.runSvgLoaderFeatureOnBreadcrumbsComp,.shouldUseResponsiveImages,.soapOffsetRefactor,.svgResolver_2,.updateRichTextSemanticClassNamesOnCorvid,.useImageAvifFormatInNativeProGallery,.useResponsiveImgClassicFixed",
    "blocksBuilderManifestGeneratorVersion": "1.129.0",
    "contentType": "application/json",
    "deviceType": "Desktop",
    "dfCk": "6",
    "dfVersion": "1.4886.0",
    "disableStaticPagesUrlHierarchy": "false",
    "editorName": "Unknown",
    "experiments": "dm_bgScrubToMotionFixer,dm_deleteLayoutOverridesForRefComponents,dm_migrateOldHoverBoxToNewFixer",
    "externalBaseUrl": "https://www.prensadanna.com.mx",
    "fileId": "6310029d.bundle.min",
    "formFactor": "desktop",
    "hasTPAWorkerOnSite": "false",
    "isClientSdkOnSite": "true",
    "isHttps": "true",
    "isInSeo": "false",
    "isMultilingualEnabled": "false",
    "isPremiumDomain": "true",
    "isTrackClicksAnalyticsEnabled": "false",
    "isUrlMigrated": "true",
    "isWixCodeOnPage": "false",
    "isWixCodeOnSite": "false",
    "language": "en",
    "languageResolutionMethod": "QueryParam",
    "metaSiteId": "5d514a92-27db-44df-83d2-57584b594a38",
    "migratingToOoiWidgetIds": "14fd5970-8072-c276-1246-058b79e70c1a",
    "module": "thunderbolt-features",
    "oneDocEnabled": "true",
    "originalLanguage": "en",
    "pageId": "a5fc37_5be91821e604070e846e614f3c524973_1709.json",
    "quickActionsMenuEnabled": "false",
    "registryLibrariesTopology": '[{"artifactId":"editor-elements","namespace":"wixui","url":"https://static.parastorage.com/services/editor-elements/1.14104.0"},{"artifactId":"editor-elements","namespace":"dsgnsys","url":"https://static.parastorage.com/services/editor-elements/1.14104.0"}]',
    "remoteWidgetStructureBuilderVersion": "1.251.0",
    "siteId": "d5bd1aa5-083a-4a15-bcd4-a8ad2280a0c3",
    "siteRevision": "1711",
    "staticHTMLComponentUrl": "https://www-prensadanna-com-mx.filesusr.com/",
    "useSandboxInHTMLComp": "false",
    "viewMode": "desktop"
}

response = requests.get(url, headers=headers, params=params)

all_links = []
try:
    data = response.json()

    # all_links = data['props']['render']['compProps']['comp-j27w46yp']['images']['link']['pageId']['title']
    count = len(all_links)

    images = data['props']['render']['compProps']['comp-j27w46yp']['images']

    for img in images:
        try:
            title = img['link']['pageId']['title']
            all_links.append(title)
        except (KeyError, TypeError):
            title = img['title']
            all_links.append(title)

except ValueError as e:
    raise Exception(f'Response error: {response.status_code} - {response.reason} - reason: {e}')

current_names = set()
count = len(all_links)

for link in all_links:
    link_text = link.strip()
    current_names.add(link_text)


existing_artists = Artist.objects.filter(website_link = website_link).order_by('id')
existing_names = set(existing_artists.values_list('artist_name', flat=True))

for name in current_names:
    artist, created = Artist.objects.get_or_create(
        artist_name=name,
        website_link = website_link,
        defaults={
            # 'website_link': website_link ,
            'agency_name': 'prensadanna',
            'date_added': today
        }
    )

missing_names = existing_names - current_names
Artist.objects.filter(website_link=website_link, date_removed__isnull=True).exclude(artist_name__in=current_names).update(date_removed=today)

print(f"🟢 Синхронізація завершена. Нові: {len(current_names - existing_names)}, Зниклі: {len(missing_names)}")