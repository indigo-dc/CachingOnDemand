
#include <set>
#include <vector>
#include <string>

#include <iostream> 
#include <string>
#include <sstream>     
#include <curl/curl.h>
#include <jsoncpp/json/json.h>

#include "smartDecisionPlugin.hh"
#include "XrdSys/XrdSysError.hh"
#include "XrdCl/XrdClURL.hh"

using namespace smartDecisionPlugin;

extern "C"
{
XrdFileCache::Decision *XrdFileCacheGetDecision(XrdSysError &log)
{
   return new Decision(log);
}
}

//==============================================================================

Decision::Decision(XrdSysError &log) : XrdFileCache::Decision(), m_log(log)
{
   m_log.Say("smartDecisionPlugin::Decision instantiated. redo");
}

Decision::~Decision()
{
   m_log.Say("smartDecisionPlugin::Decision terminated.");
}

bool Decision::ConfigDecision(const char* params)
{
   pcrecpp::StringPiece input(params);
   
   pcrecpp::RE cent("([-+]?)([^ ]+)\\s*");

   std::string opt, re;

   while (cent.Consume(&input, &opt, &re))
   {
      if (opt.empty()) opt = "+";
      m_log.Say("  Decision ", opt[0] == '+' ? "Cache: " : "Do not cache: ", re.c_str());

      m_rules.push_back(Rule(re, opt[0] == '+'));
   }

   return true;
}

//==============================================================================

static size_t WriteCallback(void *contents, size_t size, size_t nmemb, void *userp)
{
    ((std::string*)userp)->append((char*)contents, size * nmemb);
    return size * nmemb;
}

bool Decision::Decide(const std::string &lfn, XrdOss &) const
{
   m_log.Say("smartDecisionPlugin::Decision::Decide ", lfn.c_str());

   int nr = m_rules.size();

   std::ostringstream oss;
   oss << "number of rules " << nr << " ";
   m_log.Say("smartDecisionPlugin::Decision::Decide ", 
      oss.str().c_str());

   for (int i = 0; i < nr; ++i)
   {
      const Rule &r = m_rules[i];

      m_log.Say("  trying ", r.m_re.pattern().c_str());

      if (r.m_re.PartialMatch(lfn))
      {
         CURL *curl = curl_easy_init();
         // CURLcode res;
         std::string readBuffer;

         std::string url = "http://193.204.89.71:4242/resolve?lfn=";
         url.append(lfn);

 
         curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
         curl_easy_setopt(curl, CURLOPT_HTTP_VERSION, CURL_HTTP_VERSION_1_0);
         curl_easy_setopt(curl, CURLOPT_HTTPGET, 1L);
         curl_easy_setopt(curl, CURLOPT_FORBID_REUSE, 1L); 
         //curl_easy_setopt(curl, CURLOPT_CAINFO, "cacert.pem");

         curl_easy_setopt(curl, CURLOPT_VERBOSE, 1L);
         //curl_easy_setopt(curl, CURLOPT_SSL_VERIFYHOST, 0L);

         curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
         curl_easy_setopt(curl, CURLOPT_WRITEDATA, &readBuffer);

         struct curl_slist *headers=NULL; 
         headers = curl_slist_append(headers, "Accept: application/json");
         headers = curl_slist_append(headers, "Content-Type: application/json");
         headers = curl_slist_append(headers, "charsets: utf-8");
         curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);

         CURLcode res;
         res = curl_easy_perform(curl);
         curl_easy_cleanup(curl);

         if (CURLE_OK == res)
         {
            m_log.Say(readBuffer.c_str());
            Json::Value parsedFromString;
            Json::Reader reader;

            bool parsingSuccessful = reader.parse(readBuffer, parsedFromString);

            if (parsingSuccessful)
            {
               if (parsedFromString["store"].asBool())
               {
               m_log.Say("  match. returning true" );
               return true;
               }
               return false;
            }
         }
      }
   }

   return true;
}
