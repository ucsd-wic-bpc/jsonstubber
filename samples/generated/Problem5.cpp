#include <utility>
#include <vector>
#include <iostream>
#include <cstdarg>
#include <sstream>
#include <stdexcept>
#include <stack>
#include <iomanip>
#include <cstdlib>
#include <map>
#include <string>


struct result {
int dimension1Length;
int dimension2Length;
int dimension3Length;
int*** array;
};

result arrayTest(int**** Arg1, int Arg1Dimension1Length, int Arg1Dimension2Length, int Arg1Dimension3Length, int Arg1Dimension4Length, int** Arg2, int Arg2Dimension1Length, int Arg2Dimension2Length, int** Arg3, int Arg3Dimension1Length, int Arg3Dimension2Length) {

    //TODO
    result method_result;
    method_result.dimension1Length = 0;
    method_result.dimension2Length = 0;
    method_result.dimension3Length = 0;
    method_result.array = NULL;
    return method_result;
}

#ifndef JSON_OBJECT_HPP
#define JSON_OBJECT_HPP


class JSONObject {
  private:
    std::string data;

  public:
    JSONObject();
    JSONObject(std::string data);

    template <typename T>
    T cast_data();

    template <typename T>
    std::pair<T*, int> cast_to_list();
};

template <> int JSONObject::cast_data() {
  return atoi(this->data.c_str());
}

template <> double JSONObject::cast_data() {
  return atof(this->data.c_str());
}

template <> char JSONObject::cast_data() {
  return this->data[0];
}

template <> bool JSONObject::cast_data() {
  return this->data == "true";
}

template <> std::string JSONObject::cast_data() {
  return this->data;
}

#endif
#ifndef JSON_LIST_HPP
#define JSON_LIST_HPP



class JSONList : public JSONObject {
  private:
    std::vector<JSONObject*> entries;
    std::map<char, char> wrapCharacters;

    bool is_delim_char(char c);
    char get_closing_delim_from_stack(std::stack<char>& stack);
    void populate_entries_from_string(std::string str);

  public:
    JSONList(std::string data);

    JSONObject* get_item(int index);
    int get_entry_count();

    ~JSONList();
};

#endif
#ifndef JSON_PARSER_HPP
#define JSON_PARSER_HPP


class JSONParser {
  public:
    static JSONObject* get_obj_from_str(std::string str);
};

#endif

class Unifiedstr {
  public:
    template <typename T>
    static std::string to_string(T obj);

    template <typename T>
    static std::string deep_to_string(void* arr, int depth, ...);

  private:
    template <typename T>
    static std::string deep_to_string_stacked(void* arr, std::vector<int>& lengths, int curdepth=0);
};

template <typename T> std::string Unifiedstr::to_string(T obj) {
  std::ostringstream convert;
  convert << obj;
  return convert.str();
}

template <> std::string Unifiedstr::to_string(bool obj) {
  return obj ? "True" : "False";
}

template <> std::string Unifiedstr::to_string(double obj) {
  std::ostringstream convert;
  convert << std::setprecision(1) << std::fixed;
  convert << obj;
  return convert.str();
}

template <typename T>
std::string Unifiedstr::deep_to_string(void* arr, int depth, ...) {
  std::vector<int> lengths_vec;

  va_list lengths;
  va_start(lengths, depth);
  for (int i = 0; i < depth; i++) {
    lengths_vec.push_back(va_arg(lengths, int));
  }
  va_end(lengths);

  return Unifiedstr::deep_to_string_stacked<T>(arr, lengths_vec);
}

template <typename T>
std::string Unifiedstr::deep_to_string_stacked(void* arr, std::vector<int>& lengths, int curdepth) {
  if (lengths.size() == 0)
    return "";

  std::ostringstream write;
  write << "[";

  int length = lengths[curdepth];
  for (int i = 0; i < length; i++) {
    if (curdepth >= (lengths.size() - 1)) {
      write << Unifiedstr::to_string(((T*)arr)[i]);
    }
    else {
      int inner_length = lengths[curdepth+1];
      T* t_ptr = (T*) arr;
      T* inner_array = (t_ptr + (inner_length * i));
      write << Unifiedstr::deep_to_string_stacked<T>((void*)inner_array, lengths, curdepth+1);
    }

    if (i < (length - 1))
      write << ", ";
  }

  write << "]";

  return write.str();
}
int main() {
    std::string inputContents;
    getline(std::cin, inputContents);
    JSONList* argList = (JSONList*) JSONParser::get_obj_from_str(inputContents);
    JSONList* Arg1_dim4jsonlist = NULL;
    JSONList* Arg1_dim3jsonlist = NULL;
    JSONList* Arg1_dim2jsonlist = NULL;
    JSONList* Arg1jsonlist = NULL;
    Arg1jsonlist = (JSONList*) argList->get_item(0);
    int**** Arg1 = new int***[Arg1jsonlist->get_entry_count()];
    for (int i4 = 0; i4 < Arg1jsonlist->get_entry_count(); i4++) {
    Arg1_dim4jsonlist = (JSONList*) Arg1jsonlist->get_item(i4);
    int*** Arg1_dim4 = new int**[Arg1_dim4jsonlist->get_entry_count()];
    for (int i3 = 0; i3 < Arg1_dim4jsonlist->get_entry_count(); i3++) {
    Arg1_dim3jsonlist = (JSONList*) Arg1_dim4jsonlist->get_item(i3);
    int** Arg1_dim3 = new int*[Arg1_dim3jsonlist->get_entry_count()];
    for (int i2 = 0; i2 < Arg1_dim3jsonlist->get_entry_count(); i2++) {
    Arg1_dim2jsonlist = (JSONList*) Arg1_dim3jsonlist->get_item(i2);
    int* Arg1_dim2 = new int[Arg1_dim2jsonlist->get_entry_count()];
    for (int i1 = 0; i1 < Arg1_dim2jsonlist->get_entry_count(); i1++) {
    Arg1_dim2[i1] = Arg1_dim2jsonlist->get_item(i1)->cast_data<int>();
    }
    Arg1_dim3[i2] = Arg1_dim2;
    }
    Arg1_dim4[i3] = Arg1_dim3;
    }
    Arg1[i4] = Arg1_dim4;
    }
    JSONList* Arg2_dim2jsonlist = NULL;
    JSONList* Arg2jsonlist = NULL;
    Arg2jsonlist = (JSONList*) argList->get_item(1);
    int** Arg2 = new int*[Arg2jsonlist->get_entry_count()];
    for (int i2 = 0; i2 < Arg2jsonlist->get_entry_count(); i2++) {
    Arg2_dim2jsonlist = (JSONList*) Arg2jsonlist->get_item(i2);
    int* Arg2_dim2 = new int[Arg2_dim2jsonlist->get_entry_count()];
    for (int i1 = 0; i1 < Arg2_dim2jsonlist->get_entry_count(); i1++) {
    Arg2_dim2[i1] = Arg2_dim2jsonlist->get_item(i1)->cast_data<int>();
    }
    Arg2[i2] = Arg2_dim2;
    }
    JSONList* Arg3_dim2jsonlist = NULL;
    JSONList* Arg3jsonlist = NULL;
    Arg3jsonlist = (JSONList*) argList->get_item(2);
    int** Arg3 = new int*[Arg3jsonlist->get_entry_count()];
    for (int i2 = 0; i2 < Arg3jsonlist->get_entry_count(); i2++) {
    Arg3_dim2jsonlist = (JSONList*) Arg3jsonlist->get_item(i2);
    int* Arg3_dim2 = new int[Arg3_dim2jsonlist->get_entry_count()];
    for (int i1 = 0; i1 < Arg3_dim2jsonlist->get_entry_count(); i1++) {
    Arg3_dim2[i1] = Arg3_dim2jsonlist->get_item(i1)->cast_data<int>();
    }
    Arg3[i2] = Arg3_dim2;
    }
    struct result output = arrayTest(Arg1, Arg1jsonlist->get_entry_count(), Arg1_dim2jsonlist->get_entry_count(), Arg1_dim3jsonlist->get_entry_count(), Arg1_dim4jsonlist->get_entry_count(), Arg2, Arg2jsonlist->get_entry_count(), Arg2_dim2jsonlist->get_entry_count(), Arg3, Arg3jsonlist->get_entry_count(), Arg3_dim2jsonlist->get_entry_count());
    std::cout << Unifiedstr::deep_to_string<int>((void*)output.array, 3, output.dimension1Length, output.dimension2Length, output.dimension3Length) << std::endl;
}

JSONList::JSONList(std::string data) {
  this->wrapCharacters['['] = ']';
  this->wrapCharacters['"'] = '"';
  this->populate_entries_from_string(data);
}

JSONObject* JSONList::get_item(int index) {
  return this->entries.at(index);
}

int JSONList::get_entry_count() {
  return this->entries.size();
}

JSONList::~JSONList() {
  std::vector<JSONObject*>::iterator it;
  for (it = this->entries.begin(); it != this->entries.end(); it++)
    delete(*it);
}

bool JSONList::is_delim_char(char c) {
  try {
    char temp = this->wrapCharacters.at(c);
  }
  catch (const std::out_of_range& oor) {
    return false;
  }
  return true;
}

char JSONList::get_closing_delim_from_stack(std::stack<char>& stack) {
  return this->wrapCharacters.at(stack.top());
}

void JSONList::populate_entries_from_string(std::string str) {
  std::stack<char> delimiter_stack;
  std::string current_string;

  for (int i = 0; i < str.length(); ++i) {
    if (!delimiter_stack.empty() &&
        str[i] == get_closing_delim_from_stack(delimiter_stack))
      delimiter_stack.pop();
    else if (is_delim_char(str[i]))
      delimiter_stack.push(str[i]);

    // Check to see if we have reached a comma
    if ((str[i] == ',' || i == str.length() - 1) && delimiter_stack.empty()) {
      // Check if last item
      if (i == str.length() - 1) current_string.push_back(str[i]);
      this->entries.push_back(JSONParser::get_obj_from_str(current_string));
      current_string.erase(0, std::string::npos);
      continue;
    }
    current_string.push_back(str[i]);
  }
}

JSONObject* JSONParser::get_obj_from_str(std::string str) {
    // Check if surrounded by quotes, list brackets, or nothing
    if (str[0] == '[' && str[str.length() - 1] == ']')
      return new JSONList(str.substr(1, str.length() - 2));
    else if (str[0] == '"' && str[str.length() - 1] == '"')
      return new JSONObject(str.substr(1, str.length() - 2));
    else
      return new JSONObject(str);
}

JSONObject::JSONObject() {
  this->data = "";
}

JSONObject::JSONObject(std::string data) {
  this->data = data;
}

template <typename T>
std::pair<T*, int> JSONObject::cast_to_list() {
  JSONList* thisList = (JSONList*) this;
  int len = thisList->get_entry_count();
  T* arr = new T[len];
  for (int ii = 0; ii < len; ii++)
    arr[ii] = thisList->get_item(ii)->cast_data<T>();
  return std::make_pair(arr, len);
}
