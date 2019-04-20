# Baby's First JavaScript Exploitation notes

The solution code is heavily based on
[Jay Bosamiya's](https://www.jaybosamiya.com/blog)
[solution](https://www.jaybosamiya.com/blog/2019/01/02/krautflare/) for the 35C3
challenge `krautflare`.

The d8_fixes patch uses the same approach as `d8-strip-globals.patch` from
krautflare:
```patch
commit 3794e5f0eeee3d421cc0d2a8d8b84ac82d37f10d
Author: Your Name <you@example.com>
Date:   Sat Dec 15 18:21:08 2018 +0100

    strip global in realms

diff --git a/src/d8.cc b/src/d8.cc
index 98bc56ad25..e72f528ae5 100644
--- a/src/d8.cc
+++ b/src/d8.cc
@@ -1043,9 +1043,8 @@ MaybeLocal<Context> Shell::CreateRealm(
     }
     delete[] old_realms;
   }
-  Local<ObjectTemplate> global_template = CreateGlobalTemplate(isolate);
   Local<Context> context =
-      Context::New(isolate, nullptr, global_template, global_object);
+      Context::New(isolate, nullptr, ObjectTemplate::New(isolate), v8::MaybeLocal<Value>());
   DCHECK(!try_catch.HasCaught());
   if (context.IsEmpty()) return MaybeLocal<Context>();
   InitializeModuleEmbedderData(context);
```
