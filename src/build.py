"""Builds the landing page in every language from one template.

    python3 src/build.py      ->  index.html (French) and en.html (English)

Edit the design in landing.template.html and the copy below; never edit the generated
files by hand. Placeholders look like [[key]]; values may contain HTML.
"""

import html
import json
import re
from pathlib import Path

SRC = Path(__file__).resolve().parent
ROOT = SRC.parent
STAR = '<svg class="star ic fill"><use href="#i-sparkle4"/></svg>'


def hero_title(lines: list[list[str]]) -> str:
    return "".join(
        '<span class="line"><span>' + " ".join(f'<span class="w">{w}</span>' for w in words) + "</span></span>"
        for words in lines
    )


def marquee(items: list[str], outlined: bool = False) -> str:
    cls = ' class="o"' if outlined else ""
    return "".join(f"<span{cls}>{item}</span>{STAR}" for item in items)


def faq(items: list[tuple[str, str]]) -> str:
    return "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in items)


COMMON = {
    "marquee_top": marquee(["YouTube Shorts", "TikTok", "Instagram Reels", "Snapchat Spotlight"]),
}

FR = {
    "lang": "fr",
    "home_href": "index.html",
    "other_lang": "en", "other_lang_code": "EN", "other_lang_href": "en.html",
    "other_lang_label": "English version",
    "meta_description": "PogCut transforme automatiquement les meilleurs moments de tes lives et de tes vidéos en Shorts sous-titrés, publiés sur ta chaîne YouTube, TikTok et Instagram.",
    "og_title": "PogCut — Tes meilleurs moments, en Shorts, tout seuls.",
    "og_description": "Détection des moments forts, montage vertical, sous-titres, publication sur tes propres comptes. Zéro montage.",
    "nav_channel": "Ta chaîne", "nav_how": "Comment ça marche", "nav_features": "Fonctionnalités", "nav_cta": "Essai gratuit",
    "sound_label": "Activer ou couper le son", "sound_on": "Son activé", "sound_off": "Son coupé",
    "music_label": "Activer ou couper la musique", "music_on": "Musique activée", "music_off": "Musique coupée",
    "music_hint": "Un peu d'ambiance ? Active la musique",
    "hero_eyebrow": "Pour les streamers et créateurs",
    "hero_title_html": hero_title([["Tes", "meilleurs"], ["moments."], ["En", "Shorts."], ["Tout", "seuls."]]),
    "hero_sub": "PogCut repère les passages qui font réagir ton public, les monte en vertical avec des sous-titres qui claquent, et les publie <strong>sur ta propre chaîne</strong> YouTube, TikTok et Instagram. Toi, tu continues à créer.",
    "hero_cta": "Tester gratuitement 2 semaines", "hero_cta2": "Voir comment",
    "proof_channel": "Publié sur ta chaîne", "proof_edit": "Zéro montage", "proof_platforms": "4 plateformes",
    "meter_label": "Activité du chat", "share_label": "Partager", "short_handle": "@tachaine", "subscribe_label": "S'abonner",
    "ui_dislike": "Je n'aime pas", "ui_home": "Accueil", "ui_subscriptions": "Abonnements", "ui_you": "Vous",
    "ui_following": "Abonnements", "ui_foryou": "Pour toi", "ui_friends": "Amis", "ui_inbox": "Boîte de réception",
    "ui_profile": "Profil", "ui_follow": "Suivre", "ui_original_sound": "son original", "ui_original_audio": "Audio original", "toast": "Moment fort détecté !",
    "marquee_bottom": marquee(["Twitch", "Kick", "YouTube", "TikTok Live"], outlined=True),
    "channel_kicker": "Ta chaîne, tes vues",
    "channel_title": "Publié sur <span>TA</span> chaîne.<br>Pas la nôtre.",
    "channel_lead": "PogCut n'est pas une chaîne de compilation. Chaque Short sort sur tes propres comptes YouTube, TikTok et Instagram : les vues, les abonnés et la monétisation sont pour toi.",
    "own1_t": "Tes abonnés", "own1_d": "Chaque Short ramène du monde vers toi, pas vers nous.",
    "own2_t": "Ta monétisation", "own2_d": "Les vues comptent sur ta chaîne, pour ton propre programme partenaire.",
    "own3_t": "Tes droits, ton contrôle", "own3_d": "Tu gardes 100 % de ton contenu et tu coupes l'accès en un clic.",
    "stamp": "Publié sur ta chaîne", "handle": "@toncompte", "channel_sub": "Ta chaîne, alimentée par PogCut",
    "tab_home": "Accueil", "tab_videos": "Vidéos", "new_label": "NOUVEAU",
    "statement": 'Tu streames quatre heures. Ton public scrolle <span class="hl">trente secondes.</span> PogCut fait le pont.',
    "steps_kicker": "Comment ça marche", "steps_title": "Du live au Short.<br>Sans toi.",
    "step1_t": "Détecte", "step1_d": "PogCut lit ce que ton public a vraiment aimé : les passages les plus revus, les moments cités en commentaires, les pics de réaction.",
    "bubble": "« 18:22 MDR »",
    "step2_t": "Découpe", "step2_d": "Il coupe pile sur des phrases complètes : une accroche au début, la réaction à la fin. Jamais une phrase coupée en deux.",
    "cut_label": "le passage parfait",
    "step3_t": "Monte", "step3_d": "Format vertical, facecam en haut, sous-titres mot par mot, son égalisé, écran de fin. Prêt pour le scroll.",
    "edit_cap": "C'EST <b>QUOI</b> ÇA",
    "step4_t": "Publie", "step4_d": "Sur ta chaîne YouTube, ton TikTok et ton Instagram, aux heures où ton public scrolle. Avec ta validation si tu veux.",
    "aud_kicker": "Choisi par ton public", "aud_title": "Pas au hasard.<br>Par tes viewers.",
    "aud_lead": "Une IA seule ne voit pas une cascade ratée ou un fou rire. Ton public, si. PogCut croise trois signaux pour trouver les moments qui marchent vraiment.",
    "sig1_t": "La courbe « Les plus revus »", "sig1_d": "Les secondes que tes viewers rejouent encore et encore.",
    "sig2_t": "Les horodatages en commentaires", "sig2_d": "« 12:34 je suis mort » : ta commu pointe elle-même les pépites.",
    "sig3_t": "L'IA sur la transcription", "sig3_d": "Pour trouver des passages qui se comprennent seuls, avec une vraie chute.",
    "label1": "Le plus revu", "label2": "Cité 14 fois",
    "bento_kicker": "Tout est inclus", "bento_title": "Le montage d'un pro.<br>Sans lever le petit doigt.",
    "t1_t": "Sous-titres mot par mot", "t1_d": "Le style qui retient l'attention : gros, lisibles, chaque mot s'allume quand tu le prononces.",
    "karaoke_html": "".join(f"<span>{w}</span>" for w in ["Non", "mais", "t'as", "vu", "ce", "saut&nbsp;?!"]),
    "t2_t": "Facecam en haut", "t2_d": "Ta tête en haut, l'action en bas. Ou le gameplay sur fond flouté, selon le clip.",
    "t3_t": "Son égalisé", "t3_d": "Tous tes Shorts au même niveau, sans saturation, au standard de YouTube.",
    "t4_t": "Titres accrocheurs", "t4_d": "Écrits pour donner envie de rester, dans ta langue.",
    "t5_t": "Tu gardes la main", "t5_d": "Validation avant publication, accès révocable à tout moment.",
    "t6_t": "Toutes tes sources", "t6_d": "Tes clips Twitch, tes vidéos YouTube, tes rediffusions Kick et TikTok Live.",
    "t7_t": "Partout à la fois", "t7_d": "Un seul moment fort, publié sur tous tes comptes.",
    "fan_kicker": "Le résultat", "fan_title": "Prêt pour le scroll.",
    "cap1": "IL A <b>PAS</b> OSÉ", "meta1": "Le clutch le plus fou du live",
    "cap2": "C'EST <b>QUOI</b> CE SAUT", "meta2": "J'étais pas prêt #gaming",
    "cap3": "LE CHAT <b>EXPLOSE</b>", "meta3": "Le moment où tout a basculé",
    "num1": "plateformes de publication", "num2": "de montage pour toi", "num3": "Shorts par jour, à ton rythme",
    "num4": "d'essai gratuit", "num4_suffix": " j",
    "faq_kicker": "Questions", "faq_title": "Tu te demandes…",
    "faq_html": faq([
        ("Est-ce que je garde mes droits ?", "Oui, à 100 %. Tes Shorts sont publiés sur tes propres comptes, avec ton contenu. PogCut ne fait que le travail de montage et de publication."),
        ("Je peux arrêter quand je veux ?", "Oui. Tu retires l'accès depuis ton compte Google (et tes autres plateformes) en un clic, et tout s'arrête. Les Shorts déjà publiés restent à toi."),
        ("Et si un Short ne me plaît pas ?", "Active la validation : chaque Short t'attend avant de partir en ligne. Tu publies, tu modifies ou tu supprimes."),
        ("Ça marche avec Kick et TikTok Live ?", "Oui, à partir de tes rediffusions. Pour Twitch, PogCut récupère directement tes clips les plus vus."),
        ("Combien ça coûte ?", "Les 2 premières semaines sont gratuites. Ensuite, on construit une formule adaptée à ton rythme de publication, sur la base des résultats de l'essai."),
    ]),
    "final_title": "Prêt à devenir viral ?",
    "final_sub": "2 semaines d'essai gratuit, sans engagement. 10 minutes de mise en place, et tes premiers Shorts arrivent sur ta chaîne.",
    "final_cta": "Je veux mon essai gratuit", "mail_subject": "Essai%20PogCut",
    "footer_line": "© 2026 PogCut — fait par un créateur, pour les créateurs.",
    "footer_privacy": "Confidentialité", "footer_terms": "Conditions",
    "chat_calm": ["salut tout le monde", "gg", "on est là", "trop bien le setup", "first time ici", "il est chaud ce soir", "lol"],
    "chat_hype": ["POGGERS", "CLIP ÇA", "NOOON", "KEKW KEKW", "C'EST QUOI ÇA", "MDRRR", "LE SAUT", "CLIIIP"],
    "sub_words": ["C'EST", "QUOI", "CE", "SAUT", "?!"],
}

EN = {
    "lang": "en",
    "home_href": "en.html",
    "other_lang": "fr", "other_lang_code": "FR", "other_lang_href": "index.html",
    "other_lang_label": "Version française",
    "meta_description": "PogCut automatically turns the best moments of your streams and videos into captioned Shorts, published on your own YouTube, TikTok and Instagram.",
    "og_title": "PogCut — Your best moments, as Shorts, on autopilot.",
    "og_description": "Highlight detection, vertical editing, captions, publishing on your own accounts. Zero editing.",
    "nav_channel": "Your channel", "nav_how": "How it works", "nav_features": "Features", "nav_cta": "Free trial",
    "sound_label": "Turn sound on or off", "sound_on": "Sound on", "sound_off": "Sound off",
    "music_label": "Turn music on or off", "music_on": "Music on", "music_off": "Music off",
    "music_hint": "Want some vibes? Turn the music on",
    "hero_eyebrow": "For streamers and creators",
    "hero_title_html": hero_title([["Your", "best"], ["moments."], ["As", "Shorts."], ["On", "autopilot."]]),
    "hero_sub": "PogCut spots the moments your audience reacts to, cuts them vertical with captions that pop, and publishes them <strong>on your own channels</strong>: YouTube, TikTok and Instagram. You keep creating.",
    "hero_cta": "Try it free for 2 weeks", "hero_cta2": "See how",
    "proof_channel": "Posted on your channel", "proof_edit": "Zero editing", "proof_platforms": "4 platforms",
    "meter_label": "Chat activity", "share_label": "Share", "short_handle": "@yourchannel", "subscribe_label": "Subscribe",
    "ui_dislike": "Dislike", "ui_home": "Home", "ui_subscriptions": "Subscriptions", "ui_you": "You",
    "ui_following": "Following", "ui_foryou": "For You", "ui_friends": "Friends", "ui_inbox": "Inbox",
    "ui_profile": "Profile", "ui_follow": "Follow", "ui_original_sound": "original sound", "ui_original_audio": "Original audio", "toast": "Highlight detected!",
    "marquee_bottom": marquee(["Twitch", "Kick", "YouTube", "TikTok Live"], outlined=True),
    "channel_kicker": "Your channel, your views",
    "channel_title": "Posted on <span>YOUR</span> channel.<br>Not ours.",
    "channel_lead": "PogCut is not a compilation channel. Every Short goes out on your own YouTube, TikTok and Instagram accounts: the views, the subscribers and the monetization are yours.",
    "own1_t": "Your subscribers", "own1_d": "Every Short brings people to you, not to us.",
    "own2_t": "Your monetization", "own2_d": "Views count on your channel, for your own partner program.",
    "own3_t": "Your rights, your control", "own3_d": "You keep 100% of your content and can revoke access in one click.",
    "stamp": "Posted on your channel", "handle": "@yourchannel", "channel_sub": "Your channel, powered by PogCut",
    "tab_home": "Home", "tab_videos": "Videos", "new_label": "NEW",
    "statement": 'You stream for four hours. Your audience scrolls for <span class="hl">thirty seconds.</span> PogCut bridges the gap.',
    "steps_kicker": "How it works", "steps_title": "From stream to Short.<br>Without you.",
    "step1_t": "Detect", "step1_d": "PogCut reads what your audience actually loved: the most replayed parts, the moments quoted in comments, the reaction spikes.",
    "bubble": "“18:22 LMAO”",
    "step2_t": "Cut", "step2_d": "It cuts on complete sentences: a hook at the start, the reaction at the end. Never a sentence cut in half.",
    "cut_label": "the perfect clip",
    "step3_t": "Edit", "step3_d": "Vertical format, facecam on top, word-by-word captions, levelled sound, end screen. Ready for the scroll.",
    "edit_cap": "WHAT <b>WAS</b> THAT",
    "step4_t": "Publish", "step4_d": "On your YouTube channel, your TikTok and your Instagram, when your audience is scrolling. With your approval if you want.",
    "aud_kicker": "Picked by your audience", "aud_title": "Not at random.<br>By your viewers.",
    "aud_lead": "An AI alone can't see a botched stunt or a laughing fit. Your audience can. PogCut combines three signals to find the moments that actually work.",
    "sig1_t": "The “Most replayed” graph", "sig1_d": "The seconds your viewers replay again and again.",
    "sig2_t": "Timestamps in comments", "sig2_d": "“12:34 I'm dead”: your community points out the gems itself.",
    "sig3_t": "AI on the transcript", "sig3_d": "To find clips that make sense on their own, with a real punchline.",
    "label1": "Most replayed", "label2": "Quoted 14 times",
    "bento_kicker": "Everything included", "bento_title": "Pro-level editing.<br>Without lifting a finger.",
    "t1_t": "Word-by-word captions", "t1_d": "The style that holds attention: big, readable, each word lights up as you say it.",
    "karaoke_html": "".join(f"<span>{w}</span>" for w in ["Bro", "did", "you", "see", "that", "jump?!"]),
    "t2_t": "Facecam on top", "t2_d": "Your face on top, the action below. Or gameplay on a blurred background, depending on the clip.",
    "t3_t": "Levelled sound", "t3_d": "All your Shorts at the same level, no clipping, at YouTube's standard.",
    "t4_t": "Catchy titles", "t4_d": "Written to make people stay, in your language.",
    "t5_t": "You stay in control", "t5_d": "Approval before publishing, access you can revoke at any time.",
    "t6_t": "All your sources", "t6_d": "Your Twitch clips, your YouTube videos, your Kick and TikTok Live replays.",
    "t7_t": "Everywhere at once", "t7_d": "One highlight, published on all your accounts.",
    "fan_kicker": "The result", "fan_title": "Ready for the scroll.",
    "cap1": "HE <b>ACTUALLY</b> DID IT", "meta1": "The craziest clutch of the stream",
    "cap2": "WHAT <b>WAS</b> THAT JUMP", "meta2": "Wasn't ready for this #gaming",
    "cap3": "CHAT <b>EXPLODES</b>", "meta3": "The moment everything changed",
    "num1": "publishing platforms", "num2": "of editing for you", "num3": "Shorts a day, at your pace",
    "num4": "free trial", "num4_suffix": " days",
    "faq_kicker": "Questions", "faq_title": "You might wonder…",
    "faq_html": faq([
        ("Do I keep my rights?", "Yes, 100%. Your Shorts are published on your own accounts, with your content. PogCut only does the editing and publishing work."),
        ("Can I stop whenever I want?", "Yes. Revoke access from your Google account (and your other platforms) in one click and everything stops. Shorts already published stay yours."),
        ("What if I don't like a Short?", "Turn on approval: every Short waits for you before going live. Publish it, edit it or delete it."),
        ("Does it work with Kick and TikTok Live?", "Yes, from your replays. For Twitch, PogCut fetches your most viewed clips directly."),
        ("How much does it cost?", "The first 2 weeks are free. After that, we build a plan that fits your publishing pace, based on the trial results."),
    ]),
    "final_title": "Ready to go viral?",
    "final_sub": "2-week free trial, no commitment. 10 minutes of setup, and your first Shorts land on your channel.",
    "final_cta": "Get my free trial", "mail_subject": "PogCut%20trial",
    "footer_line": "© 2026 PogCut — made by a creator, for creators.",
    "footer_privacy": "Privacy", "footer_terms": "Terms",
    "chat_calm": ["hey everyone", "gg", "we're here", "sick setup", "first time here", "he's on fire tonight", "lol"],
    "chat_hype": ["POGGERS", "CLIP IT", "NOOO", "KEKW KEKW", "WHAT WAS THAT", "LMAOOO", "THE JUMP", "CLIIIP"],
    "sub_words": ["WHAT", "WAS", "THAT", "JUMP", "?!"],
}

OUTPUTS = {"index.html": FR, "en.html": EN}
MEDIA = ROOT / "media"


def media_slots() -> dict:
    """Real demo media, used wherever the files exist (see src/prepare_media.py).
    Missing files keep the animated mock-up, so the page always builds."""
    has = lambda name: (MEDIA / name).exists()
    video = 'muted playsinline loop preload="auto"'
    slots = {"body_class": "", "hero_media": ""}
    if has("hero-source.mp4") and has("hero-short.mp4"):
        slots["body_class"] = "has-real-hero"
        slots["hero_media"] = (f'<video class="real real-land" src="media/hero-source.mp4" {video} autoplay></video>'
                               f'<video class="real real-vert" src="media/hero-short.mp4" {video}></video>')
    for i in (1, 2, 3):
        ok = has(f"short-{i}.mp4")
        poster = f' poster="media/short-{i}.jpg"' if has(f"short-{i}.jpg") else ""
        slots[f"phone{i}_class"] = "has-video" if ok else ""
        slots[f"phone{i}_media"] = f'<video src="media/short-{i}.mp4"{poster} {video} autoplay></video>' if ok else ""
    for i in range(1, 7):
        ok = has(f"thumb-{i}.jpg")
        slots[f"thumb{i}_class"] = "real" if ok else ""
        slots[f"thumb{i}_style"] = (f'style="background: url(media/thumb-{i}.jpg) center / cover"' if ok else "")
    return slots


def short_credit(i: int) -> dict:
    """Handle and caption of the creator shown in phone i (media/short-i.json, written by
    prepare_media.py), so the app chrome credits the right person."""
    path = MEDIA / f"short-{i}.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def render(template: str, strings: dict) -> str:
    values = {**COMMON, **media_slots(), **strings}
    for i in (1, 2, 3):
        credit = short_credit(i)
        values[f"phone{i}_handle"] = html.escape(credit.get("handle", "")) or strings["handle"]
        values[f"phone{i}_caption"] = html.escape(credit.get("caption", "")) or strings[f"meta{i}"]

    def value(match: re.Match) -> str:
        key = match.group(1)
        if key not in values:
            raise KeyError(f"missing translation: {key}")
        v = values[key]
        # Lists are injected into the script as JSON; "</" is escaped so a string can
        # never close the <script> tag.
        return json.dumps(v, ensure_ascii=False).replace("</", "<\\/") if isinstance(v, list) else v

    out = re.sub(r"\[\[([a-z0-9_]+)\]\]", value, template)
    unused = set(strings) - set(re.findall(r"\[\[([a-z0-9_]+)\]\]", template))
    if unused:
        raise KeyError(f"unused translations: {sorted(unused)}")
    return out


def main() -> None:
    template = (SRC / "landing.template.html").read_text(encoding="utf-8")
    if set(FR) != set(EN):
        raise KeyError(f"languages differ: {sorted(set(FR) ^ set(EN))}")
    used = [k for k, v in media_slots().items() if v and not k.endswith(("_class", "_style"))]
    print("media:", ", ".join(used) or "none (animated mock-ups)")
    for name, strings in OUTPUTS.items():
        (ROOT / name).write_text(render(template, strings), encoding="utf-8")
        print(f"✓ {name}")


if __name__ == "__main__":
    main()
